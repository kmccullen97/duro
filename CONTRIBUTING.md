# Contributing

First of all, thank you for taking the time to contribute to this project.

For general questions, comments or other discussions create a [discussion](https://github.com/kmccullen97/duro/discussions).

### Find a bug?

Report a bug using [Github Issues](https://github.com/kmccullen97/duro/issues).

### Have a feature request?

Look through current [enhancement](https://github.com/kmccullen97/duro/labels/enhancement) issues to make sure there isn't already a issue for the feature you want.

If there isn't already an issue for the feature you want, create a new issue.

Add a :+1: to issues you want implemented.

### Creating a pull request

Pull requests are welcome! All pull requests must be associated with an issue.

New to the project? Check out the [good first issue](https://github.com/kmccullen97/duro/labels/good%20first%20issue) label.

### Running the app

- clone the repo `git clone https://github.com/kmccullen97/duro.git`
- create the virtual environment `python3 -m venv .venv`
- load the virtual environment `source .venv/bin/activate`
- install dependencies `pip3 install -r requirements.txt`
- run the project `ENV=dev python3 -m duro` or `make run`

Other Actions
- Linting `flake8 .` or `make lint`
- Setup pre-commit
   - make executable `chmod +x .githooks/pre-commit`
   - add git hooks path `git config core.hooksPath .githooks`

When `ENV` is set to `dev` the config file and data file locations are in the `./data` directory.
