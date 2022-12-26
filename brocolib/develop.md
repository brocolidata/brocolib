# **brocolib** Development

## Create a new brocolib package
We are using [Poetry](https://python-poetry.org/docs/) to package the libaries and manage their dependencies. In order to create a library (Make sure you are in a running VSCode remote container (step 4 of [Quickstart](/README.md#quickstart) and with a terminal located in `/brocolib`) :
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


## Run documentation website
Make sure you are in `/brocolib` and run 
```
portray server
```