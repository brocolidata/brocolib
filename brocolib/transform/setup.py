from setuptools import setup, find_packages

VERSION = '0.0.5'
DESCRIPTION = 'Data Transformation Brocoli Library'
LONG_DESCRIPTION = 'Brocoli Library for Data Transformation'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="brocolib_transform", 
        version=VERSION,
        author="Brocoli",
        author_email="contact.brocoli@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            "dbt-bigquery==1.3.0",
            "dbt-core==1.3.1"
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