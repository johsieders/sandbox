# sandbox

You'll find some of my favourite programs in my sandbox.

I started rewriting some of them using GPT 4.1: I gave GPT 4.1 instructions and copied and pasted the results into PyCharm.

The results can be found in sandbox/stepfunctions and test/stepfunctions. There are two important files in StepFunctions: stepfun.py and intervals.py. The stepfun_n.py files show how I progressed from a basic solution to the final result. There are two important test drivers in tests/test_stepfunctions: test_stepfun_f.py and test_intervals_b.py.

The important thing is that I didn't edit a single line. The code was generated entirely automatically. It took me around 10 hours to create this small library. The generated code was generally very good. GPT made a few subtle mistakes and one significant performance error. I never edited the code myself. Instead, I told GPT to fix the problem, sometimes providing a hint, and it always did so.

GPT generated all the test cases. The generated code was good up to a point; many of the expected values were incorrect. This isn't surprising, as it is difficult for a general-purpose generator to outperform a special-purpose testee. I corrected the incorrect expected values, and that was the only manual editing I did. Next, I instructed GPT to generate test cases in the style of test_stepfun_f.py and test_intervals_b.py. This was a huge step forward; they passed (ignoring minor issues) on the first run.

The test cases run on a MacBook Air M4 in around 15 seconds. They also run on a Windows 11 PC, Codespace and a Raspberry Pi 5, albeit a bit slower.
