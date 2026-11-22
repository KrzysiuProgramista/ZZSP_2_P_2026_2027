# Exercise 3 – tearDown with files

### What was built

- `FileStore` (in `file_store.py`) with `save(data, path)` and `load(path)`, using the `json` module.
- `TestFileStore` (in `test_file_store.py`) with five tests:
  1. save then load
  2. load a missing file (`FileNotFoundError`)
  3. save an empty dictionary
  4. overwrite an existing file
  5. load a corrupted file (`json.JSONDecodeError`)

### How setUp and tearDown work together

- `setUp()` asks the system for a unique temporary file name with `tempfile.mkstemp()` and then removes the empty file, so every test starts with a name but no file.
- `tearDown()` deletes the file **if it exists**. The check is needed because some tests never create the file (for example the missing-file test).
- `tearDown()` runs after every test, even if the test failed, so a failing test cannot leave a file behind.

### Confirming that no file is left behind

All temporary files start with the prefix `filestore_test_`. The script `check_no_leftovers.py` counts such files in the system temp folder, runs the tests, and counts again:

```bash
python check_no_leftovers.py
```

```text
Ran 5 tests in 0.002s

OK

Temp files before the run: 0
Temp files after the run:  0
OK - the tests passed and no test file was left behind.
```

**Observation:** The number of files is the same before and after the run, so `tearDown()` cleans up correctly.
