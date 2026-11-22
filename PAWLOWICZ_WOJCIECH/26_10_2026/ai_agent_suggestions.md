# Suggestions for future AI agents debugging `debugging_lab.py`-style tasks

Written after working through the five injected bugs in this exercise, for
any AI agent asked to do something similar.

1. **Run before you read.** Execute the failing case first and capture its
   exact output verbatim. Don't reason about the code from static reading
   alone — two of the five bugs (cases 2 and 4) produce output that looks
   plausible or even "SOLVED" on casual reading, and only running
   (and in case 2's case, a *second*, pointed test) exposes the problem.

2. **"No crash" is not "no bug."** A program that completes and prints a
   plausible-looking answer on the one test maze provided can still be
   wrong. When asked to "fix the bugs," check the code's *logic* against
   its *contract* (here: correct 4-directional bounds checking), not just
   whether today's test case happens to pass.

3. **The crash site and the defect site are usually different places.**
   Don't edit the line that appears in the traceback or the line where
   `solve()` returns the wrong status without first tracing *backwards*
   to find which earlier computation produced the bad value that led
   there. In this lab, the win condition, the neighbor coordinates, and
   the dedup check all failed somewhere other than the "obvious" spot.

4. **Prefer one well-placed trace over many prints.** Reuse any
   instrumentation hooks the program already offers (here, `print_state`
   and `--trace`) instead of sprinkling ad hoc `print()` calls everywhere.
   It keeps the diff small and keeps "do not rewrite the whole program"
   honest.

5. **State your hypothesis in words before changing code.** Write (or, as
   an agent, narrate) what you expect to observe if your hypothesis is
   correct, run the diagnostic, and only then edit. Guess-and-check wastes
   turns and tends to introduce a second bug while "fixing" the first.

6. **After fixing, re-test on more than the original input.** A fix that
   only works on the maze that happened to reveal the bug may be coincidentally
   correct (see case 1's wall-shifted goal check, which "worked" only
   because of where the wall happened to sit). Always add at least one
   independent test case — a different maze is better than rerunning the
   same one.

7. **Keep the debugging log honest and short.** A one-paragraph record of
   (observed effect -> hypothesis -> evidence -> root cause -> fix) per
   bug is more useful to a grader or a future reader than a long narrative
   of trial and error. State the conclusion, back it with the specific
   line(s) of evidence, and move on.

8. **Don't "fix" a symptom by special-casing the test data.** E.g. for
   case 1 it would be tempting to just special-case the exact wall cell;
   the actual fix is to restore the correct general comparison
   (`current == self.goal`), which is what the rest of the lab's rules
   ("do not remove the search algorithm") are protecting against.
