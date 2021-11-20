![Brocoli Logo](brocoli_logo.png)
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
3. Open a Remote Window  *(click on blue button left-down corner and click "Reopen in Container)*

## Rebuild brocolib source distribution+wheel.
**Prerequisites** : Make sure all packages mentioned in *src/\*/setup.py* (in `install_requires`) are also in *docker_build/requirements.txt* and that the Docker image is fresh.

Open a terminal inside the container and run 
```
python3 setup.py sdist bdist_wheel
```