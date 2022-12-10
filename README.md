# Bakus Service
[![Coverage Status](https://coveralls.io/repos/github/SirSeim/bakus-service/badge.svg?branch=main)](https://coveralls.io/github/SirSeim/bakus-service?branch=main)

⚓️ Service that powers Bakus

## Development
Setup your environment for development

### Step 1: Install machine dependencies
Can skip these instructions if you already have `pyenv`, `postgres` installed. Use `brew` to install these.

We use pyenv for setting up python environment. Full instructions available [from `pyenv`](https://github.com/pyenv/pyenv).
```bash
brew install pyenv pyenv-virtualenv
```
Setup shell profile with `pyenv` init lines. Here's the example for `.bash_profile`
```bash
export PYENV_ROOT=$HOME/.pyenv
export PATH=$PYENV_ROOT/shims:$PATH

# Complete pyenv setup
if command -v pyenv 1>/dev/null 2>&1; then
  eval "$(pyenv init -)"
  eval "$(pyenv virtualenv-init -)"
fi
```

This project uses `postgres` as its database. `brew services` is our preferred way to run it.
```bash
brew install postgres
brew services start postgres
```

### Step 2: Setup project specifics
Using [pgAdmin](https://www.pgadmin.org/download/) (or some other postgres client tool), add a user and database for bakus-service to use:
* Database name: `bakus-service`
* User: `bakus`
* Password: `bakus`

This project uses Python 3.10, which we should install using pyenv
```bash
# pyenv will show more versions for 3.10
# use the latest patch version offered
pyenv install 3.10.4
```

Setup virtualenv using pyenv. We use the name `bakus-service` to have consistent naming.
```bash
pyenv virtualenv 3.10.4 bakus-service
```
Set that new pyenv version (pyenv treats virtualenvs as just addition versions) as the one to use for our project. This assumes your shell is set to the top level of the repo.
```bash
pyenv local bakus-service
```

### Step 3: Setup project for dev work
Install project dependencies. This installs the main dependencies in addition to the ones for dev work.
```bash
pip install -r requirements-dev.txt
```

Setup pre-commit to ensure proper code formatting
```bash
pre-commit install
```

### Step 4: Setup Transmission for remote access
TBD

## Dev Work Tips

If using PyCharm, take a look at [PyCharm Tips](/docs/pycharm-tips.md)
