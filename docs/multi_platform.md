# Multi-Platform Development: Mac and Raspberry Pi 5

How the `sandbox` project is developed on a Mac and run, tested and compared on a headless
Raspberry Pi 5 — with one code base, one git repository and (almost) one environment.

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
          └──────────── ssh jean@192.168.178.115 '...' ─────────────┘
```

**Master and mirror.**

- The Mac copy is the only source of truth and the only git repository. Commits and pushes happen
  there.
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

| | Mac | Pi 5 |
|---|---|---|
| CPU / OS | Apple silicon, macOS | Cortex-A76 (4 cores), Raspberry Pi OS (Debian, aarch64) |
| torch | PyPI build, GPU via MPS | CPU-only build (`torch+cpu`) |
| Accelerator | Apple GPU (MPS) | Hailo-8 (compiled networks, no torch) |
| Seed packages | — | `pip` kept in `.venv` (created with `--seed`) |

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
- `[tool.uv.sources]` + `[[tool.uv.index]]`: on Linux, torch comes from the PyTorch CPU index.
  The default PyPI torch for linux-aarch64 is a CUDA build that drags in ~3.3 GB of NVIDIA
  libraries no Pi can use.

`uv.lock` is *universal*: one file resolves for macOS and Linux at the same time (both torch
variants are in it). `uv sync` makes a venv match the lock exactly, adding, upgrading and removing
packages. `pyproject.toml` and `uv.lock` are always committed together.

### 3.3 SSH

The Mac reaches the Pi as `jean@192.168.178.115` with key `~/.ssh/id_ed25519`; no password. On
the Pi, `jean` has passwordless sudo (`/etc/sudoers.d/010_pi-nopasswd`), so administrative
commands can also be run remotely (`ssh … 'sudo -n …'`).

Non-interactive SSH commands (`ssh pi 'cmd'`, PyCharm, scripts) get a minimal `PATH`
(`/usr/local/bin:/usr/bin:/bin`) — `~/.local/bin` is *not* on it. Scripts therefore use full
paths (`~/.local/bin/uv`, `~/sandbox/.venv/bin/python`).

### 3.4 PyCharm on the Mac

PyCharm runs only on the Mac. Two features connect it to the Pi:

- **Deployment server "pi5"** (SFTP): maps the project root to `/home/jean/sandbox`, with
  *automatic upload: always*. Every file saved in PyCharm is uploaded immediately. Excluded:
  `.venv`, `.git`, `.idea`, `sandbox.egg-info`.
- **SSH interpreter "Pi5 Python 3.14.7"**: `/home/jean/sandbox/.venv/bin/python` on the Pi, with
  the deployment "pi5" as its sync folder. Run configurations, the test runner and the debugger
  execute on the Pi when this interpreter is selected. PyCharm copies its helper scripts to
  `~/.pycharm_helpers` (~75 MB) on the Pi; that directory is needed and refreshed on PyCharm
  upgrades.

Switching the project interpreter between the Mac `.venv` and "Pi5 Python 3.14.7" decides where
code runs; the code itself is the same.

### 3.5 Scripts

| Script | Where | Purpose |
|---|---|---|
| `tools/sync_pi.sh` | Mac | `rsync -rc --delete` of the project to the mirror, same excludes as "pi5". `-n` = dry run. |
| `remote-setup.sh` | Pi | `uv sync --locked`: build or update `.venv` from `uv.lock`. |
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
  ssh jean@192.168.178.115 'cd ~/sandbox && .venv/bin/python -m pytest tests/py4alg -n auto -q'
  ```
- **Pi, on the Pi** (standalone): `cd ~/sandbox && source .venv/bin/activate && pytest …`

The full suite takes well over 5 minutes even with `-n auto` on the Mac, much longer on the Pi.
During development, run targeted modules. Slow or fragile cases are marked `stress`; deselect them
with `-m "not stress"`.

### 4.4 Compare results and execution times

```bash
python tools/compare_hosts.py tests/py4alg --check-sync
```

runs the target on both machines one after the other, reads pytest's JUnit XML reports and lists
the tests by Pi time together with the Pi/Mac ratio. Orientation: collecting the 31,222 tests takes
5 s on the Mac and 11.5 s on the Pi; `test_polynomials.py` runs in 2.2 s vs. 3.4 s.

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
ssh jean@192.168.178.115 'bash ~/sandbox/remote-setup.sh' # Pi .venv := uv.lock
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


## 5. PyCharm: Where Things Live

| What | Where |
|---|---|
| Deployment server "pi5" (host, key, root path, mappings, excludes) | Tools → Deployment → Configuration (same as Settings → Build, Execution, Deployment → Deployment) |
| Auto-upload on/off, delete behaviour | Tools → Deployment → Automatic Upload; Tools → Deployment → Options |
| Manual upload, compare with the Pi | Tools → Deployment → Upload to pi5 / Sync with Deployed to pi5; Browse Remote Host |
| SSH connections | Settings → Tools → SSH Configurations |
| Project interpreter (Mac `.venv` or "Pi5 Python 3.14.7") | Settings → Python → Interpreter; status bar, lower right |
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

**6.3 Python 3.14 is installed but invisible ("only 3.11 and 3.12").**
*Cause:* uv installs into `~/.local/bin`, which is only on the `PATH` of interactive login shells.
PyCharm and `ssh pi 'cmd'` don't see it.
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
*Cause:* `ssh pi 'pkill -f pattern'` also matches the remote shell whose command line contains the
pattern; and pytest-xdist respawns killed workers.
*Fix:* list with `ps -eo pid,args | grep "[p]ytest"`, then `kill <pid>` — controller first, then
workers.

**6.8 A test runs forever although it has a timeout.**
*Case:* `test_axioms.py::test_int[Complex > Matrix > Fraction > FieldPolynomial > Fraction >
NativeInt]`, `@pytest.mark.timeout(10)`, ran for over 38 minutes in a full xdist run on the Pi.
Alone it times out correctly after 10 s on both machines, with or without xdist; so does the whole
module `test_axioms.py` run by itself on the Pi (4 workers, 11 min, no hang).
*Diagnosis:* `sudo uvx py-spy dump --pid <worker>` shows where a live Python process is (here:
nested fraction/polynomial GCDs, pure Python). Cause of the missing timeout: open (§9).
*Mitigation:* the case is marked `stress`.

**6.9 Git operations on the Pi.**
*Don't.* The mirror has no `.git`. Pulling there would create a second source of truth that
`sync_pi.sh --delete` then silently overwrites.


## 7. Design Decisions

**Mirror instead of a second clone.** Earlier, the Pi had its own git clone (`git pull` per
session). Two repositories drift, need their own git access on the Pi, and invite quick fixes on the wrong
machine. A mirror has exactly one direction of flow and nothing to merge.

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


## 9. Open Issues

- **Test tiers.** A fast tier (< 1 min) that checks everything broadly, and a stress tier
  (< 10 min). The `stress` marker is the first step.
- **Timeouts in long xdist workers** (§6.8): why pytest-timeout did not fire in the full run.
  `test_axioms.py` alone does not hang, so another module run earlier in the same worker is the
  prime suspect.
- **Silent timeouts.** In that module alone, 188 of 585 cases hit their 10 s timeout on the Pi.
  `check_axioms` catches the timeout and records a "graceful failure", so these cases count as
  passed, and the module takes 11 minutes. They are stress candidates, and a passed test currently
  does not mean the axioms were fully checked.
- **Hailo from the venv.** `python3-hailort` is an apt package for the system Python 3.11; the
  project venv (3.14) cannot import it yet.
- **Python 3.15** once torch and highspy publish wheels.
