# Multi-Platform Development: Mac, Raspberry Pi 5 and Windows

How the `sandbox` project is developed on a Mac and run, tested and compared on a headless
Raspberry Pi 5 — with one code base, one git repository and (almost) one environment. A Windows
machine with an NVIDIA GPU works on its own clone of the same repository with the same uv
environment (§10); it is independent of the Mac/Pi pair.

State: September 2026 (Python 3.14.7, uv 0.12.19, PyCharm 2026.2).


## 1. Purpose

The Mac is where code is written: fast, with PyCharm, git and an agent (Claude Code). The Pi 5 is
a second, very different machine: ARM Linux, 4 cores, 16 GB RAM, no display, a Hailo-8 AI
accelerator instead of a GPU. Running the same code on both

- exposes platform assumptions (paths, macOS-only libraries, MPS vs. CPU, wheel availability),
- shows how the code behaves with scarce resources (the full test suite is much slower on the Pi),
- prepares for work that only the Pi can do (Hailo, GPIO, long unattended runs).

The goal is **cross development**: all editing on the Mac, execution on either machine, with as
little ceremony as possible.


## 2. Architecture

```
         Mac (master)                                        Pi 5 (mirror)
  ~/PycharmProjects/sandbox                           ~/sandbox
  ┌──────────────────────────┐  PyCharm auto-upload   ┌──────────────────────────┐
  │ git repo ─push─▶ GitHub  │  ───── (SFTP) ──────▶  │ plain files, no git      │
  │ PyCharm, Claude Code     │    tools/sync_pi.sh    │ no PyCharm, headless     │
  │ .venv  (uv, 3.14.7)      │  ───── (rsync) ─────▶  │ .venv  (uv, 3.14.7)      │
  └──────────────────────────┘                        └──────────────────────────┘
          │        ▲                                                ▲
          │        └───── SSH interpreter: run / debug / test ──────┘
          └───────────────────── ssh pi5 '...' ─────────────────────┘
```

**Master and mirror.**

- The Mac copy is the source of truth for the Pi and the only git repository of the Mac/Pi pair.
  Commits and pushes happen there. (The Windows machine has its own clone of the GitHub repository
  and never touches the Pi, §10.)
- `~/sandbox` on the Pi is a *mirror*: a file-by-file copy of the Mac project minus local state
  (`.venv`, `.git`, `.idea`, caches). It is never edited, never pulled, never pushed. It has no
  `.git`, on purpose, so nobody is tempted.
- The mirror is written only by the Mac (PyCharm or rsync). Every change on the Mac shows up on the
  Pi within seconds (PyCharm) or on demand (rsync).

**Independence.** The Pi does not know the Mac exists. `~/sandbox` with its own `.venv` is a
complete, standalone installation: you can log into the Pi and run `pytest` without the Mac being
switched on. The Mac, in turn, drives the Pi remotely over SSH: from PyCharm (remote interpreter),
from scripts, or from the terminal.

**One environment, allowed differences.** Both machines run CPython 3.14.7 installed by uv, and both
venvs are built from the same `uv.lock`, so every package has the same version on both. Differences
are deliberate and declared in `pyproject.toml`:

| | Mac | Pi 5 | Windows (own clone, §10) |
|---|---|---|---|
| CPU / OS | Apple silicon, macOS | Cortex-A76 (4 cores), Raspberry Pi OS (Debian, aarch64) | Intel x86-64, Windows |
| torch | PyPI build, GPU via MPS | CPU-only build (`torch+cpu`) | CUDA 13.0 build (`torch+cu130`) |
| Accelerator | Apple GPU (MPS) | Hailo-8 (compiled networks, no torch) | NVIDIA GPU (CUDA) |
| Seed packages | — | `pip` kept in `.venv` (created with `--seed`) | — |

Everything else — Python version, library versions, test collection (31,222 tests) — is identical.


## 3. Components

### 3.1 Python and uv

[uv](https://docs.astral.sh/uv/) installs Python itself and manages the venv.

- `.python-version` (`3.14.7`) pins the interpreter; uv downloads it if missing.
- uv's Pythons live in the user's home, not in the system: on the Pi
  `~/.local/share/uv/python/cpython-3.14.7-…`, reachable as `~/.local/bin/python3.14`.
  A link `/usr/local/bin/python3.14 → ~/.local/bin/python3.14` makes it visible to non-interactive
  SSH sessions and to PyCharm's interpreter detection (see §6.3).
- The system Pythons on the Pi (3.11 in `/usr/bin`, 3.12/3.13 in `/usr/local/bin`) are not used by
  the project. Leave them alone: Raspberry Pi OS and apt packages (e.g. Hailo's `python3-hailort`)
  depend on 3.11.

### 3.2 pyproject.toml and uv.lock

`pyproject.toml` declares everything; `uv.lock` pins it:

- `[project] dependencies`: the libraries (numpy, pandas, torch, sympy, highspy, pypsa, …) with
  lower bounds.
- `[dependency-groups] dev`: the test tools (pytest, pytest-xdist, pytest-timeout,
  pytest-benchmark). Installed by default by `uv sync`.
- `[tool.setuptools.packages.find]`: packages `sandbox*` and `tests*` (tests import each other as
  `tests.py4alg…`). `uv sync` installs the project in editable mode, so `import sandbox…` works
  from any directory.
- `[tool.pytest.ini_options]`: `testpaths = ["tests"]` and the `stress` marker.
- `[tool.uv.sources]` + `[[tool.uv.index]]`: torch per platform. On Linux it comes from the
  PyTorch CPU index — the default PyPI torch for linux-aarch64 is a CUDA build that drags in
  ~3.3 GB of NVIDIA libraries no Pi can use. On Windows it comes from the CUDA 13.0 index
  (`cu130`) for an NVIDIA GPU; the PyPI build for Windows would be CPU-only. macOS keeps the PyPI
  build (MPS). The former helper scripts `cuda.bat`, `cuda.sh` and `mps.sh` (pip installs) are
  gone; `uv sync` on each machine picks the right build.

`uv.lock` is *universal*: one file resolves for macOS, Linux and Windows at the same time (all three
torch variants are in it). `uv sync` makes a venv match the lock exactly, adding, upgrading and removing
packages. `pyproject.toml` and `uv.lock` are always committed together.

### 3.3 SSH

The Mac reaches the Pi as `pi5`, an alias in `~/.ssh/config`:

```
Host pi5
    HostName raspberrypi5.local      # mDNS name, follows a new DHCP address
    User jean
    HostKeyAlias 192.168.178.115     # host key stays filed under the original IP
    ConnectTimeout 5

Host pi5 github.com                  # key from the 1Password SSH agent
    IdentityAgent "~/Library/Group Containers/2BUA8C4S2C.com.1password/t/agent.sock"
    IdentityFile ~/.ssh/id_ed25519_1p.pub
    IdentitiesOnly yes
```

The private key exists only in 1Password (personal vault "Private", item "SSH key: Mac → pi5,
GitHub"); it was generated there and never touched the disk. `~/.ssh/id_ed25519_1p.pub` is the
public key; it only tells ssh which of the agent's keys to offer. The same key opens the Pi and
GitHub. 1Password asks once per app (Terminal, PyCharm) for approval and remembers it until it
locks; while 1Password is locked, every SSH connection — auto-upload, `sync_pi.sh`, `git push` —
waits for Touch ID. The previous key (a file without passphrase) was revoked on the Pi and GitHub
and deleted in September 2026.

`tools/sync_pi.sh`, `tools/compare_hosts.py` and `tools/check_pi.py` use `pi5`; if the Pi's
address changes, none of them needs an edit. PyCharm's SSH configuration (§5) uses `pi5` as
well, with authentication "OpenSSH config and authentication agent". On the Pi, `jean` has passwordless sudo (`/etc/sudoers.d/010_pi-nopasswd`), so administrative
commands can also be run remotely (`ssh … 'sudo -n …'`).

Non-interactive SSH commands (`ssh pi5 'cmd'`, PyCharm, scripts) get a minimal `PATH`
(`/usr/local/bin:/usr/bin:/bin`) — `~/.local/bin` is *not* on it. Scripts therefore use full
paths (`~/.local/bin/uv`, `~/sandbox/.venv/bin/python`).

### 3.4 PyCharm on the Mac

PyCharm runs only on the Mac. It has exactly two interpreters for the project, one per machine,
and a deployment server that connects it to the Pi:

- **uv interpreter "Python 3.14.7 uv"**: the Mac `.venv`. Because it is a uv-type interpreter,
  PyCharm's package window (Python Packages) runs uv, so installing a package there updates
  `pyproject.toml` and `uv.lock` exactly like `uv add` in the terminal.
- **Deployment server "pi5"** (SFTP): maps the project root to `/home/jean/sandbox`, with
  *automatic upload: always*. Every file saved in PyCharm is uploaded immediately. Excluded:
  `.venv`, `.git`, `.idea`, `sandbox.egg-info`.
- **SSH interpreter "Pi5 Python 3.14.7"**: `/home/jean/sandbox/.venv/bin/python` on the Pi, with
  the deployment "pi5" as its sync folder. Run configurations, the test runner and the debugger
  execute on the Pi when this interpreter is selected. PyCharm copies its helper scripts to
  `~/.pycharm_helpers` (~75 MB) on the Pi; that directory is needed and refreshed on PyCharm
  upgrades.

Switching the project interpreter between "Python 3.14.7 uv" and "Pi5 Python 3.14.7" decides
where code runs; the code itself is the same. Why the two interpreters are of different types is
explained in §7.

### 3.5 Scripts

| Script | Where | Purpose |
|---|---|---|
| `tools/sync_pi.sh` | Mac | `rsync -rc --delete` of the project to the mirror, same excludes as "pi5". `-n` = dry run. |
| `remote-setup.sh` | Pi | `uv sync --locked`: build or update `.venv` from `uv.lock`. |
| `tools/check_pi.py` | Mac | Read-only health check of SSH, mirror, Pi venv, PyCharm leftovers and PyCharm's server/interpreter; prints the fix for each failure (§4.7). |
| `tools/compare_hosts.py` | Mac | Run the same pytest target on both machines, compare per-test times; `--check-sync` reports mirror drift. |

`sync_pi.sh` compares by checksum and deletes files that no longer exist on the Mac, so it
repairs everything auto-upload misses.


## 4. Use Cases

### 4.1 Edit, add or delete a program file, a test or a subproject

1. Edit in PyCharm on the Mac. Saving uploads the file to the Pi.
2. For a new subproject: a package directory under `sandbox/` (with `__init__.py`) and its tests
   under `tests/`. Package discovery (`sandbox*`, `tests*`) and the editable install pick it up
   without reinstalling.
3. **Anything not saved through PyCharm** — deletions, renames in the shell, `git checkout`,
   `git pull`, edits by Claude Code — is *not* uploaded. Run `tools/sync_pi.sh` afterwards. When
   in doubt, run it anyway: it only copies what differs.

### 4.2 Sync master and mirror

```bash
tools/sync_pi.sh -n     # show what differs (nothing printed = in sync)
tools/sync_pi.sh        # fix it
```

Rule of thumb: before any comparison between Mac and Pi, and for any unexplained Pi discrepancy,
first run `tools/sync_pi.sh -n`.

### 4.3 Run or debug a test

- **Mac:** Mac interpreter selected, run or debug as usual; or `pytest tests/…` in the terminal
  with the venv active.
- **Pi, from PyCharm:** select "Pi5 Python 3.14.7", then run or debug the same run
  configuration. Breakpoints work; the process runs on the Pi.
- **Pi, from the Mac terminal** (no PyCharm needed):
  ```bash
  ssh pi5 'cd ~/sandbox && .venv/bin/python -m pytest tests/py4alg -n auto -q'
  ```
- **Pi, on the Pi** (standalone): `cd ~/sandbox && source .venv/bin/activate && pytest …`

The full suite (about 31,400 tests) takes about 1 minute with `-n auto` on the Mac and about 3 minutes on the Pi
(September 2026, after `test_axioms.py` went to depth 4).
During development, run targeted modules; `tests/py4alg` takes about 10 s on the Mac. The `stress`
marker is registered for slow cases (deselect with `-m "not stress"`) but currently unused.

Output and reports:

- Print output of passed tests: `-rP` in the summary, or `-s` live (not with `-n auto`).
- `tests/py4alg` writes its exception report (graceful failures of the axiom checks) to
  a new file per run, `reports/<YYYYMMDD-HHMMSS>_py4alg_exceptions_<host>.txt`, on the machine
  that ran the tests; the timestamp prefix sorts the files chronologically, old reports are kept.
  This also works under PyCharm's test runner (the file is written in `pytest_sessionfinish`); with
  the Pi interpreter selected, the report lands on the Pi. `reports/` is gitignored and excluded
  from `sync_pi.sh`, so the Pi's reports survive a sync.
- What the report covers: `check_axioms` (`tests/py4alg/check_protocols.py`) picks the checks by
  protocol — field, Euclidean ring, ring, or abelian group (the last since September 2026; before,
  group-only types such as `ECpoint` ran no checks at all) — plus the order axioms if the elements
  are comparable. A violated axiom or a numerical problem (division by zero, overflow, domain error,
  an int too long to print, recursion) is reported per case and the loop continues; any other
  exception is reported under the check's name and the next check runs; a timeout is reported as
  `timeout`. The test itself passes: the report, not the test status, tells whether the axioms hold.
- Benchmarks are disabled by default (`addopts = "--benchmark-disable"`): benchmarked tests run once
  as plain tests. Measure with `--benchmark-enable --benchmark-only` (without `-n auto`);
  `--benchmark-autosave` stores each run in `.benchmarks/<platform>/`, `--benchmark-compare`
  compares against the last one.

### 4.4 Compare results and execution times

```bash
python tools/compare_hosts.py tests/py4alg --check-sync
```

runs the target on both machines one after the other, reads pytest's JUnit XML reports and lists
the tests by Pi time together with the Pi/Mac ratio. Orientation: collecting the 31,222 tests takes
5 s on the Mac and 11.5 s on the Pi; `test_polynomials.py` runs in 2.2 s vs. 3.4 s.

Results: after running `tests/py4alg` on both machines, compare the exception reports, e.g.
`diff "$(ls reports/*_py4alg_exceptions_*.txt | tail -1)" <(ssh pi5 'cat "$(ls sandbox/reports/*.txt | tail -1)"')`
compares the latest report of each (the first three lines — time, host, command — differ by
design). In September 2026 both machines
reported the same 30 findings.

### 4.5 Add, remove or upgrade a library

On the Mac:

```bash
uv add sympy                  # library;  uv add --dev <pkg> for test tools
uv remove sympy
uv lock --upgrade && uv sync  # upgrade everything within the bounds in pyproject.toml
```

Each command updates `pyproject.toml`, `uv.lock` and the Mac `.venv`. Then:

```bash
tools/sync_pi.sh                                          # ship pyproject.toml + uv.lock
ssh pi5 'bash ~/sandbox/remote-setup.sh'                 # Pi .venv := uv.lock
git add pyproject.toml uv.lock && git commit              # always together
```

`uv sync --locked` on the Pi refuses to run if `uv.lock` does not match `pyproject.toml` — a
guard against a half-finished change on the Mac.

### 4.6 Upgrade Python

1. Check that the heavy libraries have wheels for the new version on both platforms (torch,
   highspy: for 3.15 they did not exist as of September 2026).
2. Mac: set `.python-version` and `requires-python`, then `uv sync` (uv installs the interpreter
   and rebuilds `.venv`). Run the tests.
3. Pi: `tools/sync_pi.sh`, then `remote-setup.sh`. If `.venv` does not get rebuilt, move it aside
   first (keep it for rollback, as `~/venv-backups/…` does for the previous versions).
4. Update the link in `/usr/local/bin` and, if its name encodes the version, the PyCharm
   interpreter.

### 4.7 (Re)connect the Pi

After the Pi was switched off, rebooted, moved or reinstalled, or after the Mac was away from home:

```bash
python tools/check_pi.py
```

checks everything below in about a second and prints `OK` or `FAIL` per item, with the fix. It
changes nothing. Fix what fails, run it again, done. What it checks, and what to know beyond it:

1. **SSH to `pi5`** without a password.
   - *No answer / cannot resolve `raspberrypi5.local`:* the Pi is off or still booting (allow a
     minute).
   - *`REMOTE HOST IDENTIFICATION HAS CHANGED`:* expected after a reinstall of the Pi (new host
     key), otherwise a reason to stop and look. Remove the old key with
     `ssh-keygen -R 192.168.178.115` (the `HostKeyAlias`, §3.3) and connect again.
   - *Asks for a password:* the Mac's key is not in `~/.ssh/authorized_keys` on the Pi (e.g.
     after a reinstall): `ssh-copy-id -i ~/.ssh/id_ed25519_1p.pub pi5` (asks for the Pi password once).
   - *Hangs, then fails:* 1Password is locked or its SSH agent is off (1Password → Settings →
     Developer → "Use the SSH agent"). Unlock and approve.
   - *New address:* the scripts and PyCharm follow the mDNS name `raspberrypi5.local`
     automatically. A fixed address in the FRITZ!Box (Home Network → Network → "always assign the
     same IPv4 address") avoids surprises anyway.
2. **Pi venv**: Python version as in `.python-version`, pytest importable, packages exactly as in
   `uv.lock` (`uv sync --locked --check`). Fix: `ssh pi5 'bash ~/sandbox/remote-setup.sh'`. After
   a reinstall also repeat the setup of §3.1 and §3.3 (uv, passwordless sudo).
3. **`/usr/local/bin/python3.14` link** (§6.3).
4. **No PyCharm leftovers** on the Pi: `/tmp/pycharm_project_*`, `~/.virtualenvs` (§6.2).
5. **Mirror in sync.** Files saved in PyCharm while the Pi was unreachable were *not* uploaded,
   and PyCharm does not retry. Fix: `tools/sync_pi.sh`.
6. **PyCharm**: exactly one deployment server (`pi5`, default, mapped to `/home/jean/sandbox`)
   and exactly one Pi interpreter (`/home/jean/sandbox/.venv/bin/python`, using `pi5`). If the
   interpreter shows as invalid, select it once (Settings → Python → Interpreter); PyCharm
   reconnects and refreshes `~/.pycharm_helpers` if necessary. Never add a new interpreter to
   "repair" the connection (§6.2). The script reads PyCharm's files; changes made in the settings
   dialog show up once it is closed with OK.

Smoke test afterwards: `python tools/compare_hosts.py tests/py4alg/test_polynomials.py --check-sync`.

From outside the home network, `pi5` is not reachable at all; see §8.


## 5. PyCharm: Where Things Live

| What | Where |
|---|---|
| Deployment server "pi5" (host, key, root path, mappings, excludes) | Tools → Deployment → Configuration (same as Settings → Build, Execution, Deployment → Deployment) |
| Auto-upload on/off, delete behaviour | Tools → Deployment → Automatic Upload; Tools → Deployment → Options |
| Manual upload, compare with the Pi | Tools → Deployment → Upload to pi5 / Sync with Deployed to pi5; Browse Remote Host |
| SSH connections | Settings → Tools → SSH Configurations |
| Project interpreter ("Python 3.14.7 uv" or "Pi5 Python 3.14.7") | Settings → Python → Interpreter; status bar, lower right |
| All interpreters (add, rename, remove) | Settings → Python → Interpreter → Show All |
| Sources, excluded folders | Settings → Project Structure |

When adding a Pi interpreter, choose *existing* `/home/jean/sandbox/.venv/bin/python` and set the
sync folder to `/home/jean/sandbox`. PyCharm's default is a fresh copy in `/tmp/pycharm_project_…`
(see §6.2).


## 6. What Can Go Wrong

Each entry happened at least once.

**6.1 `pytest` not found on the Pi.**
*Cause:* the PyCharm interpreter is the bare Python (`/usr/local/bin/python3.14`), not the venv.
uv's Pythons have no packages; the libraries are in `~/sandbox/.venv`.
*Fix:* use `/home/jean/sandbox/.venv/bin/python`.

**6.2 PyCharm starts copying the project.**
*Cause:* a newly added SSH interpreter gets its own sync folder `/tmp/pycharm_project_<id>` and a
full upload; with a uv-type interpreter PyCharm even runs `uv init` there.
*Fix:* remove that interpreter, delete `/tmp/pycharm_project_*`, and point the interpreter at
`/home/jean/sandbox`.
*Variant (after a reboot of the Pi):* `cd: /tmp/pycharm_project_<id>/tests/…: No such file or
directory`. The Pi interpreter had silently become a uv-type interpreter
(`~/.virtualenvs/sandbox`, no pytest) with its own deployment server
`jean@192.168.178.115:22 key` mapped to `/tmp/pycharm_project_<id>`, and that server was the
default for auto-upload. It worked as long as the copy in `/tmp` existed; the reboot emptied `/tmp`.
*Fix:* do **not** create a new interpreter — the wizard defaults to a `/tmp` sync folder and starts
copying the whole project, `.venv` included (cancel it via the progress bar). Instead, in
Settings → Python → Interpreter → Show All, delete every interpreter whose path is not
`/home/jean/sandbox/.venv/bin/python` and keep the one that is, even if it shows a stale version;
in Tools → Deployment → Configuration, delete every server except `pi5` and make `pi5` the default.
Then remove the leftovers on the Pi: `rm -rf /tmp/pycharm_project_* ~/.virtualenvs/sandbox`.

**6.3 Python 3.14 is installed but invisible ("only 3.11 and 3.12").**
*Cause:* uv installs into `~/.local/bin`, which is only on the `PATH` of interactive login shells.
PyCharm and `ssh pi5 'cmd'` don't see it.
*Fix:* `sudo ln -s /home/jean/.local/bin/python3.14 /usr/local/bin/python3.14`, or use full paths.

**6.4 The Pi runs stale code.**
*Cause:* auto-upload only sees saves in PyCharm. `git checkout`, shell edits, agent edits and
deletions are missed (once 9 stale files had piled up).
*Fix:* `tools/sync_pi.sh`.

**6.5 Installing torch downloads gigabytes.**
*Cause:* PyPI's linux-aarch64 torch is the CUDA build.
*Fix:* the CPU index in `[tool.uv.sources]` (§3.2). Do not install torch with plain `pip` on the
Pi.

**6.6 `sudo` suddenly asks for a password.**
*Cause:* a broken file in `/etc/sudoers.d` (a display name with a space instead of the login name
`jean`) is skipped with a syntax warning.
*Fix:* write sudoers files only through `visudo -cf <file>` (syntax check) and install them with
mode 0440. A deleted or broken file can only be repaired with the password.

**6.7 Killing remote processes kills the SSH session.**
*Cause:* `ssh pi5 'pkill -f pattern'` also matches the remote shell whose command line contains the
pattern; and pytest-xdist respawns killed workers.
*Fix:* list with `ps -eo pid,args | grep "[p]ytest"`, then `kill <pid>` — controller first, then
workers.

**6.8 A test runs forever although it has a timeout.**
*Case:* `test_axioms.py::test_int[Complex > Matrix > Fraction > FieldPolynomial > Fraction >
NativeInt]`, `@pytest.mark.timeout(10)`, ran for over 38 minutes in a full xdist run on the Pi.
Alone it times out correctly after 10 s on both machines, with or without xdist; so does the whole
module `test_axioms.py` run by itself on the Pi (4 workers, 11 min, no hang).
*Diagnosis:* `sudo uvx py-spy dump --pid <worker>` shows where a live Python process is (here:
nested fraction/polynomial GCDs, pure Python). Cause of the missing timeout: open (§11).
*Resolution:* `test_axioms.py` now builds type towers of depth 4 instead of 6 (57 instead of 585
cases); the case no longer exists, and `tests/py4alg` runs in about 10 s on the Mac.

**6.9 Git operations on the Pi.**
*Don't.* The mirror has no `.git`. Pulling there would create a second source of truth that
`sync_pi.sh --delete` then silently overwrites.

**6.10 Two Mac interpreters for the same venv.**
*Symptom:* PyCharm lists a "Python" (virtualenv-type) and a "uv" interpreter; both work.
*Cause:* both point to `~/PycharmProjects/sandbox/.venv/bin/python` — left over from before the
uv migration. Running code and tests is identical; only package management differs. The
virtualenv type installs with pip: the venv has no pip since the migration (`uv sync` removed
it), and a package installed that way is missing from `uv.lock`, so the next `uv sync` removes
it again and the Pi never gets it.
*Fix:* Settings → Python → Interpreter → Show All: delete the virtualenv-type entry (this removes
only PyCharm's entry, not the venv) and keep the uv one.


## 7. Design Decisions

**Mirror instead of a second clone.** Earlier, the Pi had its own git clone (`git pull` per
session). Two repositories drift, need their own git access on the Pi, and invite quick fixes on the wrong
machine. A mirror has exactly one direction of flow and nothing to merge. The Windows machine is a
different case: a full development machine with its own editor and its own work, so it gets a clone
(§10) — but it never feeds the Pi.

**uv and a lock file instead of `requirements.txt`.** `requirements.txt` was unpinned: each machine
installed whatever was newest on the day of installation. `uv.lock` gives both machines the same
versions, one file resolves both platforms, and platform differences (torch) are declared, not
improvised with installer flags. uv also replaced building Python from source on the Pi
(`./configure && make altinstall`, once needed for 3.12).

**Python outside the system.** uv's Pythons live in the user's home; the OS Python stays
untouched. Upgrades cannot break Raspberry Pi OS, and several versions coexist.

**SSH on the local network, not Raspberry Pi Connect.** Pi Connect offers screen sharing and a
browser shell, but no SSH endpoint: no rsync, no PyCharm, no scripted access. It remains the
fallback when SSH is broken. Access from outside the home network is discussed in §8.

**uv interpreter on the Mac, plain SSH interpreter on the Pi.** The Pi's `.venv` is built by uv
too (`remote-setup.sh` = `uv sync --locked`), but PyCharm treats it as a plain remote interpreter,
on purpose:

- *Packages are managed on the Mac only.* A uv-type Pi interpreter would let PyCharm's package
  window run uv on the Pi and change `pyproject.toml` and `uv.lock` in the mirror — edits that
  never reach git and that the next `sync_pi.sh` overwrites. The Pi interpreter is an execution
  target, nothing more; its packages follow `uv.lock` via `remote-setup.sh`.
- *PyCharm's uv wizard for remote targets does not adopt an existing environment.* It creates its
  own environment (in `~/.virtualenvs`) and a new sync folder in `/tmp/pycharm_project_…`, and may
  run `uv init` there (§6.2). That is exactly the second copy of the project the mirror design
  avoids.

**No torch acceleration on the Pi.** There is no GPU that torch supports on the Pi: the Hailo-8
(and Coral, Hailo-10H) run compiled networks for inference, the VideoCore GPU has no torch backend,
and external GPUs over the single PCIe lane are experimental. torch on the Pi is CPU-only by
design.


## 8. Remote Access from Outside the Home Network

The setup assumes that Mac and Pi share the home network (`192.168.178.x`). Away from home there
are two options.

**Raspberry Pi Connect** (already installed and signed in) gives a desktop or a shell in the
browser via connect.raspberrypi.com. It needs nothing else but carries no SSH: no rsync, no
PyCharm, no scripts. Good for occasional checks and emergencies.

**Tailscale** creates a private network ("tailnet") across one's own devices, based on WireGuard.
Each device gets a stable address (`100.x.y.z`) and a name such as `pi5.<tailnet>.ts.net` that
work from anywhere, without port forwarding on the router. Tailscale's servers only handle logins
and distribute public keys; data flows directly between the devices, or — when firewalls prevent
that — through Tailscale relays, still end-to-end encrypted. Everything in this paper would keep
working; only the host address in `tools/sync_pi.sh`, `tools/compare_hosts.py` and the PyCharm
server "pi5" would change. Free for personal use.

*Safety.*

- WireGuard encryption; private keys never leave the devices; Tailscale cannot read the traffic.
- The coordination server is the trust anchor: since it distributes public keys, it could in
  principle add a device to the tailnet. *Tailnet Lock* closes this gap (new devices must be
  signed by an existing one).
- Login is through an identity provider (Google, Apple, GitHub, Microsoft): whoever controls that
  account controls the tailnet — use two-factor authentication.
- By default every device may reach every other one; access rules restrict that.
- Clients are open source, the coordination server is not; *Headscale* is a self-hosted
  replacement.

*Interference with other VPNs.* Tailscale coexists with most VPNs, but not easily with one that

- uses the same address range `100.64.0.0/10` (corporate zero-trust clients such as Cloudflare
  WARP use `100.96.0.0/12`, inside that range; some mobile carriers and hotel networks too),
- takes over all DNS (Tailscale needs its own resolver for the `.ts.net` names), or
- routes all traffic through its own tunnel.

Typical symptoms: `.ts.net` names do not resolve, the Pi is unreachable while the other VPN is on,
or company resources break. Exceptions would have to be configured in the other VPN — for a
corporate VPN, centrally by IT.

*Further points.*

- Disable key expiry for the headless Pi in the admin console; otherwise its key expires after 180
  days and it silently drops off the tailnet.
- *Tailscale SSH* (logins instead of SSH keys) is optional; plain SSH over the tailnet keeps the
  current setup unchanged.
- Negligible CPU and memory use, even on the Pi.

**Decision.** At home nothing is needed. Away from home, Pi Connect covers occasional access. On a
company-managed Mac with a corporate VPN, installing Tailscale is a question for IT first — both
because of the conflicts above and because of policy. Alternatively, use Tailscale from a private
device.


## 9. More Compute for Training

Neither machine is built for training large networks: the Pi's Hailo-8 only runs compiled,
already trained networks, and the Mac's GPU (MPS) has limits. Codespaces are CPU machines for
development, not for training. The options, in the order to try them:

**0. Make the most of the Mac.** MPS handles small and medium networks, and Apple silicon's
unified memory holds fairly large models. Profile one run first; try lower precision, smaller
batches, fewer epochs. Fine-tuning a pretrained model instead of training from scratch often
turns a cluster job into a laptop job.

**1. Free or cheap notebook GPUs, for experiments.** Kaggle (free GPU, limited hours per week) and
Google Colab (free tier, paid tiers with better GPUs). Good for finding out whether a model is worth
scaling up; awkward for long runs (sessions are cut off) and outside the git + uv workflow.

**2. GPUs by the hour, for real runs.**

- *GPU rental* (RunPod, Lambda, Vast.ai): a Linux machine with a GPU, reached by SSH and billed by
  the hour. Clone the repo, `uv sync`, train, copy the results out, shut the machine down — the same
  workflow as a Codespace. The cheapest route to serious GPUs.
- *Modal*: runs single Python functions on GPUs, billed by the second, no server to manage.
- *AWS, Google Cloud, Azure*: the widest choice, but more setup (GPU quotas usually have to be
  requested first) and higher prices.

Save checkpoints regularly (cheap "spot" machines can be stopped at any time), keep the data next to
the GPU instead of uploading it again and again, and always shut machines down — an idle GPU costs
as much as a busy one.

**Prerequisite: torch for Linux with a GPU.** Windows already gets the CUDA build (§3.2), but
`[tool.uv.sources]` gives *every* Linux
machine the CPU build of torch. On a rented GPU machine that means torch without CUDA — no error,
just no GPU. Before the first GPU run the rule has to be split: Linux on ARM (the Pi) keeps the CPU
build, Linux on x86-64 gets the CUDA build. Codespaces (x86-64, no GPU) should stay on CPU, or every
new Codespace downloads about 3 GB of CUDA libraries; uv can express this with a machine marker or
with separate `cpu`/`gpu` extras.


## 10. Windows Machine (Own Clone)

**Role.** A Windows PC (Intel x86-64, NVIDIA GPU) works on its own git clone of
`github.com/johsieders/sandbox`, like any collaborator's machine: pull, work, commit, push. It runs
the same uv environment as the Mac — same Python, same `uv.lock`, same package versions — except
that torch is the CUDA build. There is no mirroring and no Pi access: `tools/sync_pi.sh`,
`tools/check_pi.py`, `tools/compare_hosts.py` and `remote-setup.sh` are Mac/Pi tools and are not
used on Windows.

**Setup** (PowerShell):

1. Install git (Git for Windows) and uv:
   `winget install astral-sh.uv`, or `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`.
2. NVIDIA driver: `nvidia-smi` must show "CUDA Version: 13.0" or higher; otherwise update the
   driver. A CUDA toolkit is *not* needed — the torch wheel brings its own CUDA runtime.
3. Clone: `git clone git@github.com:johsieders/sandbox.git` (with an SSH key of this machine
   registered on GitHub — e.g. generated in 1Password, whose SSH agent also runs on Windows) or via
   HTTPS.
4. `cd sandbox; uv sync` — uv downloads Python 3.14.7 (`.python-version`), creates `.venv` and
   installs exactly `uv.lock`, torch from the `cu130` index (`[tool.uv.sources]`, §3.2). Every
   locked package has a ready-made Windows wheel for Python 3.14 (checked September 2026); nothing
   is compiled.
5. Check:
   ```
   uv run python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
   # 2.14.0+cu130 True
   uv run pytest tests/py4alg -n auto
   ```
6. PyCharm: open the folder and choose the existing uv environment `.venv\Scripts\python.exe`
   (uv type, so the package window runs uv, §3.4). In a terminal, `.venv\Scripts\Activate.ps1`
   activates the venv; `uv run …` works without activation.

**Working with two clones.**

- Pull before starting, push when done — on both machines. `uv run` and `uv sync` update the venv
  automatically when a pull changed `pyproject.toml` or `uv.lock`.
- A dependency added on Windows (`uv add …`) changes `pyproject.toml` and the universal `uv.lock`
  for all platforms. On the Mac: `git pull`, `uv sync`, then `tools/sync_pi.sh` and
  `remote-setup.sh` on the Pi — `git pull` on the Mac is a change outside PyCharm, so auto-upload
  misses it (§6.4).
- Line endings: Git for Windows converts to CRLF on checkout by default. Shell scripts
  (`remote-setup.sh`, `tools/sync_pi.sh`) must stay LF, or they break on the Mac and the Pi.
  `.gitattributes` (`* text=auto`, `*.sh text eol=lf`) makes this independent of each machine's
  git settings: the repository stores LF, and shell scripts are checked out with LF everywhere.

**Differences to Mac and Pi.**

- *Timeouts.* pytest-timeout interrupts a test with `SIGALRM` on macOS and Linux; Windows has no
  such signal, so it uses a timer thread that dumps the stacks and ends the whole process
  (`os._exit(1)`). `check_axioms` therefore cannot report a Windows timeout as a graceful
  `timeout`: without xdist the test session ends, with `-n auto` the worker dies, the test is
  reported as failed and xdist starts a new worker.
- *Reports.* A new exception report per run in `reports\<timestamp>_py4alg_exceptions_<host>.txt`,
  as on the other machines; `reports/` is gitignored.
- *Scripts.* The Mac/Pi scripts are bash; they are neither needed nor run on Windows.


## 11. Open Issues

- **Test tiers.** A fast tier (< 1 min) that checks everything broadly, and a stress tier
  (< 10 min). The `stress` marker is registered for this but not used yet.
- **Timeouts in long xdist workers** (§6.8): why pytest-timeout did not fire in the full run.
  `test_axioms.py` alone does not hang, so another module run earlier in the same worker is the
  prime suspect.
- **Silent timeouts.** At depth 6, 188 of 585 cases hit their 10 s timeout on the Pi.
  `check_axioms` records a timeout as a "graceful failure", so such a case counts as passed; a
  passed test does not by itself mean the axioms were fully checked — the exception report does.
  At depth 4 only one timeout remains (`SymbolicInt`, 5 s).
- **Hailo from the venv.** `python3-hailort` is an apt package for the system Python 3.11; the
  project venv (3.14) cannot import it yet.
- **Python 3.15** once torch and highspy publish wheels.
