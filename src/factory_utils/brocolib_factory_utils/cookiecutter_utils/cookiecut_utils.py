from github import Github
import os
from typing import Union


client_organisation = os.getenv("CLIENT_ORGANISATION") # ${{ inputs.client_organisation }}
client_github_token= os.getenv("CLIENT_GITHUB_TOKEN")
client_repo = os.getenv("CLIENT_REPO")  # ${{ inputs.client_new_repo }}
gh_workspace = os.getenv("GH_WORKSPACE")
brocoli_organisation = os.getenv("BROCOLI_ORGANISATION")
brocoli_github_token = os.getenv("BROCOLI_GITHUB_TOKEN")
brocoli_templ_repo = os.getenv("BROCOLI_TEMPL_REPO")


for x in [client_organisation, client_github_token, client_repo, gh_workspace, brocoli_organisation, brocoli_github_token, brocoli_templ_repo]:
    if x is None:
        vname = [name for name in globals() if globals()[name] is x and name!='x' and name!='__doc__']
        raise ValueError(f'{vname} variable must be set or given')


def gith_connect( 
    token: Union[None , str] = client_github_token,
    organisation: Union[None , str] = client_organisation,
):
    """
    function that connects to github with token for user or organisation

    Args:
        token (Union[None , str], optional): GitHub token. Defaults to None.
        organisation (Union[None , str], optional): organisation (or user) name. Defaults to None.

    Returns:
        class: github.Organization.Organization represents Organizations
    """

    token = client_github_token
    organisation = client_organisation
   
    g = Github(token)
    org = g.get_organization(organisation)

    return org


