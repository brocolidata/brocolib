![Brocolib Logo](https://drive.google.com/uc?export=view&id=1NcTPDHMy35vJfAeZowYeD00byWlHhXrs)
[![Pytest CI](https://github.com/brocolidata/brocolib/workflows/Pytest%20CI/badge.svg)](https://github.com/brocolidata/brocolib/actions/workflows/pytest_CI.yml)
[![Brocolib CD](https://github.com/brocolidata/brocolib/workflows/Brocolib%20CD/badge.svg)](https://github.com/brocolidata/brocolib/actions/workflows/brocolib_CD.yml)
# **brocolib**

Brocoli Library for Data Processing

# List of packages

| Package                                            | Description                                                 |
|----------------------------------------------------|-------------------------------------------------------------|
| [brocolib_extract_load](./brocolib/extract_load)   | **E**xtract (**T**ransform) **L**oad data in a pythonic way |
| [brocolib_transform](./brocolib/transform)         | Wrapper around dbt as a transformation layer                |
| [brocolib_utils](./brocolib/utils)                 | Utilities to use Brocoli Data Platform                      |
| [brocolib_factory_utils](./brocolib/factory_utils) | Utilities to deploy Brocoli Data Platform                   |

# Installation
1. Open the [Brocoli releases page](https://github.com/brocolidata/brocolib/releases)
2. Identify the last release of the brocolib library you wish to download. At the bottom of the release you will see artifcats related to the release ; copy the URL of the `.whl` file(for example `https://github.com/brocolidata/brocolib/releases/download/utils_v_0.0.34/brocolib_utils-0.0.34-py3-none-any.whl` for `brocolib_utils==0.0.34`)
3. To install the library, run `pip install URL` (for example `pip install https://github.com/brocolidata/brocolib/releases/download/utils_v_0.0.34/brocolib_utils-0.0.34-py3-none-any.whl`)

# Development
## Prerequisites
- **Docker** (started) and docker-compose (just install Docker for Desktop if you are on laptop) 
- **VS Code** + VS Code extension [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) 


## Quickstart
1. Clone repo
2. Build the Docker Image by running
```
docker compose -f ./docker_build/docker-compose.yml build
```
3. Duplicate the `.env.example` , rename it to `.env` and replace dummy values with yours
4. Click on *Open a Remote Window* button (left-down corner) & select **Reopen in Container**

## Brocolib Development
See [Brocolib Development](/brocolib/develop.md)

## CI/CD
See [Brocolib CI/CD](.github/workflows/README.md)
