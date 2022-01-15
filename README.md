![Brocolib Logo](brocolib_github_banner.png)
# **brocolib**
Brocoli Library for Data Processing

# Installation
1. Create a GitHub [token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
2. Create an environment variable (for example *GIT_TOKEN*)  and fill its value with the token you just created
3. Then you can use
```
pip install git+https://${GIT_TOKEN}@github.com/brocolidata/brocolib/#subdirectory=src
```

# Development
## Prerequisites
- **Docker** (started) and docker-compose (just install Docker for Desktop if you are on laptop) 
- **VS Code** + VS Code extension [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) 

## Development start
The first time you clone the project and each time you make changes to the Dockerfile, rerun
```
docker compose -f docker_build/docker-compose.yml build
```

## Quickstart
1. Rename **.env.example** to **.env** and replace dummy values with yours
2. Run the **Development start** process to create the image
3. Either **Build Source without running the dev container** (below) or **Open a Remote Window**  *(click on blue button left-down corner and click "Reopen in Container)*

## Build Source without running the dev container (WARNING BELOW)
Run the following command *(replace `DIR` by either `extract_load`, `transform` or `utils`)*
```
docker compose run --rm -w /src/DIR brocolib rm -rf dist && python3 setup.py sdist bdist_wheel
```
**WARNING: when we start to have risks of breaking changes in production, remove `rm -rf` in the code above in order to keep old versions when creating new ones**

## Brocolib Development
See [Brocolib Development](/src/README.md)