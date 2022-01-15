from setuptools import setup, find_packages

VERSION = '0.0.14'
DESCRIPTION = 'Utils Brocoli Library'
LONG_DESCRIPTION = 'Brocoli Collection of high level APIs'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="brocolib_utils", 
        version=VERSION,
        author="Brocoli",
        author_email="contact.brocoli@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            "diagrams",
            "gspread",
            "pandas",
            "oauth2client",
            "ruamel.yaml",
            "google-api-python-client",
            "google-cloud-storage"
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