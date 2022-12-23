# **brocolib** Development

## Rebuild brocolib source distribution+wheel.
**Prerequisites** : Make sure all packages mentioned in *brocolib/\*/setup.py* (in `install_requires`) are also in *docker_build/requirements.txt* and that the Docker image is fresh.

Open a terminal inside the container and run 
```
python3 setup.py sdist bdist_wheel
```

## Run documentation website
*(does not work for brocolib_utils yet)*
```
portray server -m brocolib_extract_load
```
**or**
```
portray server -m brocolib_transform
```