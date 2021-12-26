from setuptools import setup, find_packages

VERSION = '0.0.13'
DESCRIPTION = 'Extract & Load Brocoli Library'
LONG_DESCRIPTION = 'Brocoli Library for Data Extraction & Load'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="brocolib_extract_load", 
        version=VERSION,
        author="Brocoli",
        author_email="contact.brocoli@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            "requests",
            "pandas",
            "fastparquet",
            "fsspec",
            "gcsfs",
            "google-cloud-storage",
            "google-cloud-bigquery",
            "google-cloud-pubsub"
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