
import os
from cookiecutter_utils import cookiecut_template

# variables for the cookicut project
cookie_templ_keys = ["DATALAKE_NAME", "DATALAKE_STORAGE_CLASS", "LANDING_NAME","LANDING_STORAGE_CLASS"] 
secrets_keys = []

# client variables for github setup
client_organisation = os.getenv("CLIENT_ORGANISATION")
client_github_token= os.getenv("CLIENT_GITHUB_TOKEN") # ${{ env.CLIENT_GITHUB_TOKEN }}
client_repo = os.getenv("CLIENT_REPO")  
local_dir = os.getenv("LOCAL_DIR") 

# brocoli variables for github setup
brocoli_organisation = os.getenv("BROCOLI_ORGANISATION")
brocolib_github_token = os.getenv("BROCOLIB_GITHUB_TOKEN")
brocoli_templ_repo = os.getenv("BROCOLI_TEMPL_REPO")



default_message_for_commit = f"created {client_repo} for {client_organisation} + cookicuted the {brocoli_templ_repo} template + added secrets + pushed"

# verify if client and brocoli variables for github are set
for x in [client_organisation, client_github_token, client_repo, local_dir, brocoli_organisation, brocolib_github_token, brocoli_templ_repo]:
    if x is None:
        vname = [name for name in globals() if globals()[name] is x and name!='x' and name!='__doc__']
        raise ValueError(f'This list of variables must be set or given {vname} ')


# creating repo and cloning locally
cookiecut_template.create_gith_repo(
    client_github_token= client_github_token,
    organisation= client_organisation,
    client_repo= client_repo
)

cookiecut_template.clone_locally(
    client_github_token= client_github_token,
    organisation= client_organisation,
    client_repo= client_repo,
    local_dir=local_dir
)



env_variables_dic = {}

for k in cookie_templ_keys:
    if os.environ.get(k) is not None:
        if k not in env_variables_dic:
            val = os.getenv(k.upper())
            env_variables_dic[k.upper()] = val


if env_variables_dic:
    cookiecut_template.cookiec_from_temp(templ_repo=brocoli_templ_repo,local_dir=local_dir,source_token=brocolib_github_token,source_organisation=brocoli_organisation, jason_dict=env_variables_dic)
else:
    cookiecut_template.cookiec_from_temp(templ_repo=brocoli_templ_repo,local_dir=local_dir,source_token=brocolib_github_token,source_organisation=brocoli_organisation)

    
#pushing changes

cookiecut_template.add_commit_push_all(local_dir=local_dir, message=default_message_for_commit)


# adding secrets to dict then add secrets to client repo


secrets_dic = {}

for k in secrets_keys:
    if os.environ.get(k) is not None:
        if k not in env_variables_dic:
            val = os.getenv(k.upper())
            secrets_dic[k.upper()] = val


if secrets_dic:
    cookiecut_template.add_gh_secret(client_github_token= client_github_token,organisation= client_organisation, client_repo= client_repo, secr_dict=secrets_dic)


print(f'{default_message_for_commit}')

