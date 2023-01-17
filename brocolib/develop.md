# **brocolib** Development
We are using [Poetry](https://python-poetry.org/docs/) to package the libaries and manage their dependencies.
All settings are defined in a `pyproject.toml` and all dependencies locked in a `poetry.lock`.

## Create a new brocolib package
Make sure you are in a running VSCode remote container (step 4 of [Quickstart](/README.md#quickstart) and with a terminal located in `/brocolib` :
- Run `poetry new --name brocolib_YOUR_LIB YOUR_LIB` (replace `YOUR_LIB` by the name of the library you wish to create) and follow the process to package your code
- Your folder should be structured like the following if you run `poetry new --name brocolib_transform transform`
```
├── README.md                   # Instructions and information about the package 
├── __init__.py
├── brocolib_transform          # Where the code is located
│   ├── __init__.py
│   └── dbt_utils.py
├── poetry.lock                 # This is generated when you install dependencies
├── pyproject.toml              # Settings of the project
└── tests                       # Where tests are located
    ├── __init__.py
    └── test_dbt_utils.py
```

# Work with a brocolib package
- When runnong poetry in the console , make sure you `cd` inside the folder of the brocolib package you are working on.
- You must activate the Python virtualenv created by Poetry for the brocolib package you are working on (the environment is created when you [install dependencies](#install-dependencies)). To display the path of your Python virtualenv, run `poetry env info -p`
- It is recommended to reopen the VS Code container inside the folder of the brocolib package you are working on.

## Manage dependencies
Make sure you `cd` in the folder of the package.

### Add a new dependency
```
poetry add a_pip_installable_package
```
### Install dependencies
```
poetry install
```
### Update dependencies
```
poetry update
```
### Remove a dependency
```
poetry remove a_pip_installable_package
```

## Documentation
The documentation is built using [Portray](https://timothycrosley.github.io/portray/).

Portray leverages all docstring in the code to build a documentation website for brocolib.

The documentation settings are defined in `/brocolib/pyproject.toml` (`brocolib` is not supposed to be a package, but we want Portray to merge all brocolib packages).

A [GitHub Action](.github/workflows/README.md#deploy-documentation) will redeploy the GitHub Pages documentation website on each PR merge on `main`.

### Run documentation website locally
Make sure you are in `/brocolib` and run 
```
portray server
```