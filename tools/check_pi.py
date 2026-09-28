"""
tools/check_pi.py

Check the Mac/Pi setup in one go (docs/multi_platform.md §4.7): SSH, mirror, the Pi's venv,
leftovers of PyCharm's /tmp trap (§6.2), and PyCharm's deployment server and Pi interpreter.
Read-only: prints OK or FAIL per check, with the fix. Exit code 1 if anything failed.

    python tools/check_pi.py
"""

import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
PI_HOST = "pi5"  # alias in ~/.ssh/config
PI_ROOT = "/home/jean/sandbox"
PI_PYTHON = f"{PI_ROOT}/.venv/bin/python"
SERVER = "pi5"  # PyCharm deployment server
JETBRAINS = Path.home() / "Library/Application Support/JetBrains"

failed = False


def report(ok: bool, what: str, fix: str = "") -> None:
    global failed
    failed |= not ok
    print(f"{'OK  ' if ok else 'FAIL'}  {what}" + ("" if ok or not fix else f"\n      → {fix}"))


def sh(cmd: list[str], timeout: int = 60) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def check_pi() -> bool:
    """Checks on the Pi, all in one SSH session. Returns False if the Pi is unreachable."""
    python_version = (PROJECT / ".python-version").read_text().strip()
    script = f"""
        echo "python=$({PI_PYTHON} -c 'import sys, pytest; print(sys.version.split()[0])' 2>&1)"
        cd {PI_ROOT} && ~/.local/bin/uv sync --locked --check >/dev/null 2>&1; echo "locked=$?"
        echo "link=$(readlink /usr/local/bin/python3.14)"
        echo "leftovers=$(ls -d /tmp/pycharm_project_* ~/.virtualenvs 2>/dev/null | tr '\\n' ' ')"
    """
    try:
        r = sh(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=5", PI_HOST, script], timeout=30)
        error = r.stderr.strip().splitlines()[-1] if r.returncode == 255 and r.stderr else None
    except subprocess.TimeoutExpired:
        error = "no answer within 30 s"
    if error:
        report(False, f"SSH to {PI_HOST}: {error}",
               "Pi off or still booting? Password prompt → ssh-copy-id; host key changed → §4.7")
        return False
    report(True, f"SSH to {PI_HOST} (no password)")
    facts = dict(line.split("=", 1) for line in r.stdout.splitlines() if "=" in line)

    report(facts.get("python") == python_version,
           f"Pi venv: Python {facts.get('python')}, pytest importable (expected {python_version})",
           f"ssh {PI_HOST} 'bash ~/sandbox/remote-setup.sh'")
    report(facts.get("locked") == "0", "Pi venv matches uv.lock",
           f"tools/sync_pi.sh, then ssh {PI_HOST} 'bash ~/sandbox/remote-setup.sh'")
    report(facts.get("link", "").endswith(".local/bin/python3.14"),
           "/usr/local/bin/python3.14 → ~/.local/bin/python3.14 (§6.3)",
           "sudo ln -s /home/jean/.local/bin/python3.14 /usr/local/bin/python3.14")
    leftovers = facts.get("leftovers", "").strip()
    report(not leftovers, "no PyCharm leftovers on the Pi" + (f": {leftovers}" if leftovers else ""),
           f"ssh {PI_HOST} 'rm -rf /tmp/pycharm_project_* ~/.virtualenvs' (after fixing PyCharm, §6.2)")
    return True


def check_mirror() -> None:
    r = sh([str(PROJECT / "tools/sync_pi.sh"), "-n"], timeout=300)
    drift = r.stdout.split()
    report(r.returncode == 0 and not drift,
           "mirror in sync" if not drift else f"mirror differs in {len(r.stdout.splitlines())} file(s)",
           "tools/sync_pi.sh")


def pycharm_options() -> Path | None:
    dirs = sorted(JETBRAINS.glob("PyCharm*/options"), key=lambda p: p.stat().st_mtime)
    return dirs[-1] if dirs else None


def check_pycharm() -> None:
    options = pycharm_options()
    if options is None:
        report(False, "PyCharm configuration not found", f"expected under {JETBRAINS}")
        return

    # Deployment servers (global) and their mappings (per project)
    servers = {s.get("id"): s.get("name") for s in ET.parse(options / "webServers.xml").iter("webServer")}
    report(list(servers.values()) == [SERVER], f"deployment servers: {', '.join(servers.values())}",
           f"Tools → Deployment → Configuration: delete all but '{SERVER}' (§6.2)")
    deployment = ET.parse(PROJECT / ".idea/deployment.xml").getroot().find("component")
    default = deployment.get("serverName")
    mappings = {p.get("name"): [m.get("deploy") for m in p.iter("mapping")] for p in deployment.iter("paths")}
    report(default == SERVER and mappings.get(SERVER) == [PI_ROOT],
           f"default server '{default}' maps to {mappings.get(default)}",
           f"'{SERVER}' as default (checkmark), mapping → {PI_ROOT}")

    # Remote interpreters: exactly one on the Pi, the project venv, synced via "pi5"
    remote = []
    for jdk in ET.parse(options / "jdk.table.xml").iter("jdk"):
        home = jdk.find("homePath").get("value")
        if home.startswith("/home/"):
            config = jdk.find(".//option[@name='webServerConfigId']")
            server = servers.get(config.get("value") if config is not None else None)
            remote.append((jdk.find("name").get("value"), home, server))
    report(len(remote) == 1 and remote[0][1:] == (PI_PYTHON, SERVER),
           "Pi interpreters: " + ("; ".join(f"'{n}' {h} via {s}" for n, h, s in remote) or "none"),
           f"keep only the one with {PI_PYTHON} via '{SERVER}'; never add a new one (§6.2)")


def main() -> int:
    if check_pi():
        check_mirror()
    check_pycharm()
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
