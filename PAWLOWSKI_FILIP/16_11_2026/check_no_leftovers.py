
import glob
import os
import subprocess
import sys
import tempfile

from test_file_store import TEMP_PREFIX

HERE = os.path.dirname(os.path.abspath(__file__))
PATTERN = os.path.join(tempfile.gettempdir(), TEMP_PREFIX + "*")


def leftovers() -> list:
    return sorted(glob.glob(PATTERN))


before = leftovers()

result = subprocess.run(
    [sys.executable, "-m", "unittest", "test_file_store"],
    cwd=HERE,
    capture_output=True,
    text=True,
)
print(result.stderr.strip())

after = leftovers()

print()
print(f"Temp files before the run: {len(before)}")
print(f"Temp files after the run:  {len(after)}")

if result.returncode == 0 and after == before:
    print("OK - the tests passed and no test file was left behind.")
else:
    print("PROBLEM - the tests failed or files were left behind:")
    for name in after:
        print("  ", name)
    sys.exit(1)
