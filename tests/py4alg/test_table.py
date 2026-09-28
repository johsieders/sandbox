# tests/py4alg/test_table.py
# Exploratory: prints the successors of Mtype.E in the protocol-transition table.
# See the output with: pytest tests/py4alg/test_table.py -rP

from sandbox.py4alg.protocols.p_table import Mtype, successors


def test_pt():
    succ = successors(Mtype.E)
    print()
    print(succ)
