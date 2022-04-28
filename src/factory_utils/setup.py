from setuptools import setup, find_packages

VERSION = '0.0.9'
DESCRIPTION = 'Factory Utils Brocoli Library'
LONG_DESCRIPTION = 'Brocoli Library for Factory workflow'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="brocolib_factory_utils", 
        version=VERSION,
        author="Brocoli",
        author_email="contact.brocoli@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            "cookiecutter",
            "PyGithub",
            "GitPython",
        ]
)