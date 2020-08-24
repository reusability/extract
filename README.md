# BigQuery GitHub Mining

# Project Setup
1. Go to `.github/workflows` and update documents depending on the projects name, the branching structures, PRs, etc.

# Environment Configurations
First, follow these instructions to set up your environment to prepare the Flatland environment on your local machine.

Download and install Python 3.7.8, if not installed yet.
```
https://www.python.org/downloads/release/python-378/
```

## Building the Project
1. **Recommended**: `Make venv-<os>` -- this should create the virtual environment -- see `venv-windows` and `venv-unix` in `Makefile` for more information,
  - (Every time) Activate the virtual environment to use it in command line:
    - Note, if you used `Make venv-<os>`, then, `<env_name>` is named `venv`.
    - Windows: `cd <yourdir>`, then `<env_name>\Scripts\activate`
    - Unix-like: `cd <yourdir>`, then `source ./<env_name>/bin/activate`
  - In your IDE such as Eclipse PyDev or PyCharm, select the Python interpreter in the
    `<env_name>/bin` or `<env_name>/Scripts` directory for your assignment project.
    - Note, the virtual environment shouldn't be pushed onto GitHub -- add to `.gitignore` if haven't already.
2. Run the `Make init` command that will initiate the `setup.py` file -- install dependencies and set's up the entire project.

## Run the Project
- Setup your Google Cloud BigQuery API Credential
- Add information into `Make run` to ensure that you can run application with make.

## Adding dependencies
- `pip install <your-package>` and add to `requirements.txt` if needed.

## Make Commands
1. `init`
2. `run`
3. `test`
4. `lint`
5. `venv-unix`
6. `venv-windows`
7. `version`
8. `clean`

# Included Tools
## General
1. Virtual Environment -- venv
2. GitHub Actions
3. Python 3.7.8
4. Makefile -- for fast installation

# Testing, Debugging and Linting.
1. PyLint -- Linting
2. Bandit -- AST-based Static Analysis
3. CodeCoverage
4. Pre-Commit -- enforce pre-commit best practice.
