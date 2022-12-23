from brocolib_factory_utils.cookiecutter_utils import cookiecut_template

CLIENT_REPO="dataplatform_functions"
CLIENT_GITHUB_TOKEN="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"
CLIENT_ORGANISATION="brocolidata-demo"
LOCAL_DIR="./dataplatform_functions"
BROCOLIB_GITHUB_TOKEN="ghp_ocjKpgMXE6KAlkMTaeKTw3G7kMhQc1xffox"
BROCOLI_ORGANISATION="brocolidata"
BROCOLI_TEMPL_REPO="factory_templates"
COOKIE_TEMP_DIRECTORY="dataplatform_functions"

if __name__ == '__main__':

    cookiecut_template.cookiec_from_temp(
        templ_repo=BROCOLI_TEMPL_REPO,
        local_dir=".",
        source_token=BROCOLIB_GITHUB_TOKEN,
        source_organisation=BROCOLI_ORGANISATION, 
        directory_name=CLIENT_REPO
    )