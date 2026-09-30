# conftest.py — pytest hooks for exception report and black box
#
# pytest discovers these hooks by name in any conftest.py on the test path.
# No registration needed — the function names are the API.
#
# With pytest-xdist (-n auto), each worker is a separate process with its own
# copy of the module-level exception_report and black_box.  The four hooks
# below transfer that data from workers to the controller for display.
#
# Without xdist (plain pytest), there is only one process; the hooks still
# work because pytest_terminal_summary falls back to the module-level data.

import json
import platform
import sys
from datetime import datetime

from tests.py4alg.check_protocols import exception_report, black_box


def pytest_configure(config):
    """Called once at startup, before test collection.

    In xdist: runs in both controller and each worker process.
    Without xdist: runs once in the single process.

    We initialise aggregation lists only on the controller (or non-xdist),
    detected by the absence of 'workerinput' (which xdist sets on workers).
    """
    if not hasattr(config, 'workerinput'):
        config._exception_report = []
        config._black_box = []


def pytest_sessionfinish(session, exitstatus):
    """Called after all tests in a process have run.

    In xdist: runs in each worker after its share of tests is done, and last on the controller,
    after all workers are down (so pytest_testnodedown has collected their data).
    Without xdist: runs once.

    Workers serialise their module-level exception_report and black_box
    into config.workeroutput, which xdist transfers to the controller.
    The controller (or the single process) writes the report file here, not in
    pytest_terminal_summary: PyCharm's test runner replaces the terminal reporter
    and never calls pytest_terminal_summary.
    """
    config = session.config
    if hasattr(config, 'workeroutput'):
        config.workeroutput['exception_report'] = json.dumps(
            [list(t) for t in exception_report])
        config.workeroutput['black_box'] = json.dumps(list(black_box))
        return
    er, bb = collected(config)
    if bb:  # check_axioms ran: keep the exception report, one file per machine
        config._report_path = write_exception_report(config, er)


def pytest_testnodedown(node, error):
    """Called on the controller each time a worker finishes (xdist only).

    Collects the serialised data that the worker stored in workeroutput
    and appends it to the controller's aggregation lists.
    """
    wo = getattr(node, 'workeroutput', {})
    er = json.loads(wo.get('exception_report', '[]'))
    node.config._exception_report.extend(tuple(t) for t in er)
    node.config._black_box.extend(json.loads(wo.get('black_box', '[]')))


def collected(config):
    """The exception report and black box of the whole run.

    In xdist: the data aggregated on the controller via pytest_testnodedown.
    Without xdist: the module-level lists, populated in-process.
    """
    er = getattr(config, '_exception_report', None) or list(exception_report)
    bb = getattr(config, '_black_box', None) or list(black_box)
    return er, bb


def pytest_terminal_summary(terminalreporter, config):
    """Called once at the very end, when pytest prints its summary (not under PyCharm's runner)."""
    er, bb = collected(config)

    if er:
        terminalreporter.section("Exception report")
        terminalreporter.write_line(f"{len(er)} graceful failure(s)")
        for check, descent, etype, msg in er:
            terminalreporter.write_line(f"  {check} [{descent}]: {etype}: {msg}")

    if bb:
        terminalreporter.section("Black box")
        terminalreporter.write_line(f"Last {len(bb)} samples checked:")
        for entry in bb:
            terminalreporter.write_line(f"  {entry}")

    path = getattr(config, '_report_path', None)
    if path:
        terminalreporter.write_line(f"Exception report written to {path.relative_to(config.rootpath)}")


def write_exception_report(config, er):
    """Write the exception report to a new file reports/<timestamp>_py4alg_exceptions_<host>.txt.

    Every run gets its own file; the timestamp prefix (YYYYMMDD-HHMMSS) sorts them
    chronologically, the host keeps the Mac's and the Pi's reports apart. reports/ is gitignored
    and excluded from the Pi mirror sync.
    """
    now = datetime.now()
    host = platform.node().split('.')[0]
    path = config.rootpath / "reports" / f"{now:%Y%m%d-%H%M%S}_py4alg_exceptions_{host}.txt"
    path.parent.mkdir(exist_ok=True)
    lines = [f"{now:%Y-%m-%d %H:%M:%S}  {host}  Python {platform.python_version()}",
             f"pytest {' '.join(sys.argv[1:])}",
             f"{len(er)} graceful failure(s)"]
    lines += [f"  {check} [{descent}]: {etype}: {msg}" for check, descent, etype, msg in er]
    path.write_text("\n".join(lines) + "\n")
    return path
