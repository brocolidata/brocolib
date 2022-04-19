from github import Github
import os
from typing import Union


client_org = os.getenv("CLIENT_ORGANISATION") # ${{ inputs.client_organisation }}
client_gh_token= os.getenv("CLIENT_GITHUB_TOKEN")
new_repo = os.getenv("CLIENT_REPO")  # ${{ inputs.client_new_repo }}
local_path = os.getenv("GH_WORKSPACE")
broc_org = os.getenv("BROCOLI_ORGANISATION")
broc_gh_token = os.getenv("BROCOLI_GITHUB_TOKEN")
broc_temp_repo = os.getenv("BROCOLI_TEMPL_REPO")



def gith_connect( 
    token: Union[None , str] = client_gh_token,
    organisation: Union[None , str] = client_org,
):
    """
    function that connects to github with token for user or organisation

    Args:
        token (Union[None , str], optional): GitHub token. Defaults to None.
        organisation (Union[None , str], optional): organisation (or user) name. Defaults to None.

    Returns:
        class: github.Organization.Organization represents Organizations
    """

    token = client_gh_token
    organisation = client_org
   
    g = Github(token)
    org = g.get_organization(organisation)

    return org


