# Brocolib CI/CD

## [pytest CI](pytest_CI.yml)

This pipeline will run on response to all PRs newly opened or synchronized.
It will run pytests tests defined in `/tests` folders inside all brocolib packages.
This pipeline must updated every time :
- [you add/remove a brocolib package](#manage-brocolib-packages)
- [add/remove an environment variable](#manage-environment-variables)

### Manage brocolib packages
When you create a new brocolib package, add the following lines in `jobs.changes.steps.filter.with.filters` (replace `PACKAGE` by the name of the new brocolib package)
```
PACKAGE:
    - 'brocolib/PACKAGE/**'
```

If you remove this package, just remove those lines.

### Manage environment variables
When you use environment variables in your project, they must be available in `pytest_CI.yaml` for your tests to run. Environment variables used by brocolib packages are defined inside `pytest_CI.yaml` in `jobs.brocolib_run_tests.env`.

When you create new environment variables in a  brocolib package :
- **if it a sensitive/secret variable** : use a [GitHub secret](https://github.com/brocolidata/brocolib/settings/secrets/actions) to store the sensitive value (give the secret the name of the environment variable) and add the following lines in `jobs.brocolib_run_tests.env` (if you environment variable is named `MY_ENV`)
```
MY_ENV: ${{ secrets.MY_ENV }}
```
- **if it isn't sensitive** : just add the environment variable directly in `jobs.brocolib_run_tests.env` (if you environment variable is named `MY_ENV` and its value `'TEST_ENV'`)
```
MY_ENV: 'TEST_ENV'
```
 
## [Brocolib CD](brocolib_CD.yml)

This pipeline will run when you merge PRs on the `main` branch.
It will deploy a GitHub Release for every new versions of brocolib packages.

## [Deploy documentation](deploy_docs.yml)

This pipeline will run when you merge PRs on the `main` branch.
It will deploy the documentation website to GitHub Pages.