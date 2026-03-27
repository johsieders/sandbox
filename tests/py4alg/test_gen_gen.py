# tests/py4alg/test_gen_gen.py

import os
from concurrent.futures import ProcessPoolExecutor, as_completed

from sandbox.py4alg.protocols.p_euclidean_ring import EuclideanRing
from sandbox.py4alg.protocols.p_field import Field
from sandbox.py4alg.protocols.p_ring import Ring
from sandbox.py4alg.util.gen_samples import gen_ints, gen_floats, gen_complex_, gen_gen
from sandbox.py4alg.util.utils import compose, set_test_seed


def _classify(sample):
    """Return the name of the most specific check for a sample's algebraic type."""
    if isinstance(sample, Field):
        return 'check_fields'
    elif isinstance(sample, EuclideanRing):
        return 'check_euclidean_rings'
    elif isinstance(sample, Ring):
        return 'check_rings'
    else:
        return 'check_abelian_group'


def _run_check(samples, checker_name):
    """Worker function for parallel execution."""
    from tests.py4alg.check_properties import (
        check_abelian_group, check_rings, check_euclidean_rings, check_fields
    )
    checkers = {
        'check_abelian_group': check_abelian_group,
        'check_rings': check_rings,
        'check_euclidean_rings': check_euclidean_rings,
        'check_fields': check_fields,
    }
    checkers[checker_name](samples)


def _descent_str(samples):
    return ' > '.join(cls.__name__ for cls in samples[0].descent())


def test_gen_gen():
    set_test_seed()
    depth = 1
    n = 5
    print()
    result = gen_gen((gen_ints, gen_floats, gen_complex_), depth=depth, n=n)
    for g in result:
        s = compose(*g)(10, 20)
        assert len(s) == n
    print(len(result))


def test_all_types():
    set_test_seed()
    depth = 4
    n = 5

    paths = gen_gen((gen_ints, gen_floats, gen_complex_), depth=depth, n=n)

    # Generate all samples and classify
    tasks = []
    for p in paths:
        path = list(p)
        samples = compose(*path)(10, 20)
        checker_name = _classify(samples[0])
        label = _descent_str(samples)
        tasks.append((samples, checker_name, label))

    workers = os.cpu_count() or 1
    failures = []

    try:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            futures = {}
            for i, (samples, checker_name, label) in enumerate(tasks):
                future = pool.submit(_run_check, samples, checker_name)
                futures[future] = (i, label, checker_name)

            for future in as_completed(futures):
                i, label, checker_name = futures[future]
                try:
                    future.result()
                except Exception as e:
                    failures.append((i, label, checker_name, str(e)))
    except Exception:
        # Fallback to sequential if multiprocessing fails (e.g. pickling error)
        for i, (samples, checker_name, label) in enumerate(tasks):
            try:
                _run_check(samples, checker_name)
            except Exception as e:
                failures.append((i, label, checker_name, str(e)))

    print(f"\n{len(tasks)} types, {workers} cores, {len(failures)} failures")

    if failures:
        msg = f"{len(failures)}/{len(tasks)} checks failed:\n"
        for i, label, checker_name, error in sorted(failures)[:20]:
            msg += f"  [{i}] {label} ({checker_name}): {error}\n"
        if len(failures) > 20:
            msg += f"  ... and {len(failures) - 20} more\n"
        assert False, msg
