from setuptools import setup, find_packages

VERSION = '0.0.6'
DESCRIPTION = 'Brocoli Library'
LONG_DESCRIPTION = 'Brocoli Library for Data Processing'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="brocolib", 
        version=VERSION,
        author="Brocoli",
        author_email="contact.brocoli@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            "dbt",
            "requests",
            "pandas",
            "fsspec",
            "gcsfs",
            "google-cloud-storage",
            "google-cloud-bigquery"
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