export CLIENT_REPO="dataplatform_functions"
export CLIENT_GITHUB_TOKEN=""
export CLIENT_ORGANISATION="brocolidata-demo"
export LOCAL_DIR="./dataplatform_functions"
export BROCOLIB_GITHUB_TOKEN=""
export BROCOLI_ORGANISATION="brocolidata"
export BROCOLI_TEMPL_REPO="factory_templates"
export COOKIE_TEMP_DIRECTORY="dataplatform_functions"

echo "Starting test for ${LOCAL_DIR}"

python3 -m brocolib_factory_utils.cookiecutter_utils.cookiecut_template_cli