# GROUP-ddd - lab 4 - variant 3

## Project structure

- `CLI.py` -- Complete various functions.
- `CLI_test.py` -- unit tests for `CLI`.
- `CLI_api.py` -- Interface.

## Features

- support of flags with default values (python3 --version, python3 -V, python -v);
- support of position arguments (python3 module.py, cat file1 file2);
- support named arguments with default values (python3 -m module_name);
- support of sub-commands with a different set of arguments
  (e.g., git have subcommands git add, git status, git log);

- automatic help and error message generation;
- support type conversation for arguments value
  (e.g., head -n 5 conversation string “5” to int value 5);

## Contribution

- Wang Qihang -- CLI.py
- Wang Zehao -- CLI_api.py,CLI_test.py

## Changelog

- 19.06.2022 - 2
  - Add help information to the function and automatically generate help messages according to the input
- 12.06.2022 - 1
  - Wang Qihang upload CLI.py
  - Wang Zehao upload CLI_api.py,CLI_test.py
- 12.06.2022 - 0
  - Initial
