# sandbox

You'll find some of my favourite programs in my sandbox.

I started rewriting some of them using GPT 4.1: I gave GPT 4.1 instructions and copied and pasted the results into PyCharm.

- Main source: `sandbox/stepfunctions/stepfun.py` and `intervals.py`
- Progressive versions: `stepfun_n.py` files document the evolution of the solution.
- Main tests: `tests/test_stepfunctions/test_stepfun_f.py` and `test_intervals_b.py`

The important thing is that I didn't edit a single line. The code was generated entirely automatically. It took me around 10 hours to create this small library. The generated code was generally very good. GPT made a few subtle mistakes and one significant performance error. I never edited the code myself. Instead, I told GPT to fix the problem, sometimes providing a hint, and it always did so.

GPT generated all the test cases. The generated code was good up to a point; many of the expected values were incorrect. This isn't surprising, as it is difficult for a general-purpose generator to outperform a special-purpose testee. I corrected the incorrect expected values, and that was the only manual editing I did. Later, I used property-based (invariant/axiom-driven) test suites, which were much more reliable and required no manual edits. This was a huge step forward; the tests passed (ignoring minor issues) on the first run.

The full suite runs in about 15 seconds on a MacBook Air M4; also tested on Windows 11, Codespace, and Raspberry Pi 5.

*This project demonstrates how to use AI-assisted programming for rapid, mathematically sound library development.*

This project is public domain, there are no restrictions
The test tool is pytest. 
