# tools/compare_hosts.py

"""
Compare pytest execution times on the Mac and on the Raspberry Pi.

Runs the same pytest target on both machines (sequentially, so they don't
compete for the network), collects per-test durations from pytest's JUnit XML
report, and prints the tests sorted by Pi time together with the Pi/Mac ratio.

Run from the Mac, with the Mac venv active:

    python tools/compare_hosts.py                          # default: tests/py4alg
    python tools/compare_hosts.py tests/basics -k heap     # extra args go to pytest
    python tools/compare_hosts.py --top 50 --check-sync tests/stepfunctions

Notes:
- The Pi copy must be in sync with the Mac. By default ~/sandbox is used, which
  PyCharm keeps up to date by auto-upload (deployment server "pi5"); use
  --pi-root to point elsewhere. --check-sync reports differing files via
  rsync dry run.
- The Pi venv is Python 3.12, the Mac venv 3.13: ratios compare interpreter
  versions as well as hardware.
- Durations are wall-clock times as measured by pytest (setup + call + teardown).
"""

import argparse
import shlex
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent

PI_HOST = "jean@192.168.178.115"
PI_ROOT = "/home/jean/sandbox"  # PyCharm deployment mapping (server "pi5")
PI_PYTHON = "/home/jean/sandbox/.venv/bin/python"
MAC_PYTHON = str(PROJECT / ".venv/bin/python")

SYNC_EXCLUDES = [".venv", ".git", ".idea", "__pycache__", ".pytest_cache",
                 ".DS_Store", ".benchmarks", "*.egg-info", ".claude"]


def pytest_command(python: str, root: str, pytest_args: list[str]) -> str:
    """Shell command that runs pytest in root and prints the JUnit XML to stdout."""
    args = " ".join(shlex.quote(a) for a in pytest_args)
    return (f"cd {root} && report=$(mktemp) && "
            f"{python} -m pytest {args} -q -p no:cacheprovider --junitxml=$report >&2; "
            f"cat $report; rm -f $report")


def run(host: str | None, python: str, root: str, pytest_args: list[str]) -> dict[str, float]:
    """Run pytest locally (host=None) or via ssh; return {test id: seconds}."""
    cmd = pytest_command(python, root, pytest_args)
    argv = ["ssh", "-o", "BatchMode=yes", host, cmd] if host else ["bash", "-c", cmd]
    proc = subprocess.run(argv, capture_output=True, text=True)
    if not proc.stdout.strip():
        sys.exit(f"no report from {host or 'mac'}:\n{proc.stderr[-2000:]}")
    summary = proc.stderr.strip().splitlines()[-1:]  # pytest's "N passed in Xs"
    print(f"{host or 'mac':>22}: {' '.join(summary)}")
    return {f"{tc.get('classname')}::{tc.get('name')}": float(tc.get("time", 0))
            for tc in ET.fromstring(proc.stdout).iter("testcase")}


def check_sync(pi_root: str) -> None:
    """Print files that differ between the Mac project and the Pi copy."""
    excludes = [f"--exclude={e}" for e in SYNC_EXCLUDES]
    proc = subprocess.run(["rsync", "-rcn", "--delete", "--out-format=%i %n", *excludes,
                           f"{PROJECT}/", f"{PI_HOST}:{pi_root}/"],
                          capture_output=True, text=True)
    diff = [line for line in proc.stdout.splitlines() if line.strip()]
    if diff:
        print(f"WARNING: {len(diff)} differences between Mac and {pi_root}:")
        print("\n".join("  " + line for line in diff[:20]))
    else:
        print(f"in sync: {pi_root}")


def report(mac: dict[str, float], pi: dict[str, float], top: int) -> None:
    common = sorted(mac.keys() & pi.keys(), key=lambda k: -pi[k])
    only = (mac.keys() ^ pi.keys())
    if only:
        print(f"note: {len(only)} tests ran on only one machine (ignored)")

    print(f"\n{'mac':>9} {'pi':>9} {'pi/mac':>7}  test")
    for k in common[:top]:
        ratio = pi[k] / mac[k] if mac[k] > 0 else float("inf")
        print(f"{mac[k]:8.3f}s {pi[k]:8.3f}s {ratio:7.2f}  {k}")

    total_mac = sum(mac[k] for k in common)
    total_pi = sum(pi[k] for k in common)
    ratio = total_pi / total_mac if total_mac > 0 else float("inf")
    print(f"\n{len(common)} tests   mac {total_mac:.2f}s   pi {total_pi:.2f}s   pi/mac {ratio:.2f}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[1],
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--top", type=int, default=25, help="number of tests to list")
    parser.add_argument("--pi-root", default=PI_ROOT, help=f"project dir on the Pi (default {PI_ROOT})")
    parser.add_argument("--check-sync", action="store_true", help="rsync dry run before timing")
    args, pytest_args = parser.parse_known_args()
    pytest_args = pytest_args or ["tests/py4alg"]

    if args.check_sync:
        check_sync(args.pi_root)
    mac = run(None, MAC_PYTHON, str(PROJECT), pytest_args)
    pi = run(PI_HOST, PI_PYTHON, args.pi_root, pytest_args)
    report(mac, pi, args.top)


if __name__ == "__main__":
    main()
