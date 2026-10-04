# AI Coding Agent Guidelines: Debugging & Safe Coding

## 1. Safe Coding Habits (Catch Problems Early)
- **Use Assertions to Catch Bugs Fast:** Add quick safety checks (`assert condition`) at the start of functions and inside loops. If something goes wrong, you want the program to crash immediately where the mistake happened, rather than silently messing up data down the line.
- **Always Keep Wraparound Counters in Check:** When cycling through things that reset—like loop steps, grid directions, or repeating lists—always use modulo arithmetic (`(index + 1) % total_items`) or explicit boundary checks so you never hit an `IndexError`.
- **Avoid Unexpected Side Effects:** Functions should only do what their names say. Don't secretly change global variables, alter lists, or modify game states inside simple checker functions.

## 2. How to Track Down a Bug Step-by-Step
- **The Crash Line Isn't Always the Problem Line:** A crash (like an `IndexError`) often happens long after the real mistake occurred. If a line fails, step backward and figure out which function messed up the variable earlier in the process.
- **Log What the Program Is Doing:** When code behaves strangely, print out key variables at critical steps (like right before an `if` statement or inside a loop) to watch how the data changes.
- **Divide and Conquer the Timeline:** If a bug happens after hundreds of steps, test your program at the midpoint (e.g., check your variables at step 50). If everything looks good, the bug is in the second half; if it's already broken, search the first half.

## 3. Double-Checking Your Fixes
- **Test the Edge Cases:** Always test your code on extreme values—like $0$, negative numbers, the very first item in a list, or the last cell on a grid boundary.
- **Run the Whole Test Suite:** After fixing a bug, run all your tests again to ensure your fix didn't accidentally break another part of the program.
