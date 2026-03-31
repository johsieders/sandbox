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

    In xdist: runs in each worker after its share of tests is done.
    Without xdist: runs once (but the data is not needed here — we read
    the module-level lists directly in pytest_terminal_summary).

    Workers serialise their module-level exception_report and black_box
    into config.workeroutput, which xdist transfers to the controller.
    """
    if hasattr(session.config, 'workeroutput'):
        session.config.workeroutput['exception_report'] = json.dumps(
            [list(t) for t in exception_report])
        session.config.workeroutput['black_box'] = json.dumps(list(black_box))


def pytest_testnodedown(node, error):
    """Called on the controller each time a worker finishes (xdist only).

    Collects the serialised data that the worker stored in workeroutput
    and appends it to the controller's aggregation lists.
    """
    wo = getattr(node, 'workeroutput', {})
    er = json.loads(wo.get('exception_report', '[]'))
    node.config._exception_report.extend(tuple(t) for t in er)
    node.config._black_box.extend(json.loads(wo.get('black_box', '[]')))


def pytest_terminal_summary(terminalreporter, config):
    """Called once at the very end, when pytest prints its summary.

    In xdist: runs on the controller; reads the aggregated data collected
    via pytest_testnodedown.
    Without xdist: falls back to the module-level lists (which were
    populated in-process).
    """
    er = getattr(config, '_exception_report', None) or list(exception_report)
    bb = getattr(config, '_black_box', None) or list(black_box)

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
