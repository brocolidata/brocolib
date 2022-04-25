from setuptools import setup, find_packages

VERSION = '0.0.3'
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
        
        # keywords=['python', 'first package'],
        # classifiers= [
        #     "Development Status :: 3 - Alpha",
        #     "Intended Audience :: Education",
        #     "Programming Language :: Python :: 2",
        #     "Programming Language :: Python :: 3",
        #     "Operating System :: MacOS :: MacOS X",
        #     "Operating System :: Microsoft :: Windows",
        # ]
)