# GitHub Mining

This project is meant to allow to run static metrics analysis tools on GitHub projects.
It allows to run the analysis tool on different releases of the same projects.

# Project Setup
1. Go to `.github/workflows` and update documents depending on the projects name, the branching structures, PRs, etc.

# Environment Configurations
- First, follow these instructions to set up your environment to prepare the Flatland environment on your local machine.

Download and install Python 3.7.8, if not installed yet.
```
https://www.python.org/downloads/release/python-378/
```
- Download & install [CK Metric](https://github.com/mauricioaniche/ck) analysis tool. 
    - Please follow installation steps provided at their README page 

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
- Create `.env` file in root directory.
- Add `ck_path=/path/to/ck/source/code` to `.env` file
    - e.g `ck_path=/users/user_a/Desktop/ck/target/ck-*.*.*-SNAPSHOT-jar-with-dependencies.jar`

- Setup your Google Cloud BigQuery API Credential
- In the root directory, add `.bigquery.json` and throw in your credentials above.
- Now, you can either run the application with `make run` or use an IDE such as PyCharm.

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
