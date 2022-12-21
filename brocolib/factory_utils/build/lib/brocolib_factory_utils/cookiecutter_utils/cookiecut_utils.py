from github import Github
import os
from typing import Union


def gith_connect( 
    token: str,
    organisation: str,
):
    """
    function that connects to github with token for user or organisation

    Args:
        token (Union[None , str], optional): GitHub token. Defaults to None.
        organisation (Union[None , str], optional): organisation (or user) name. Defaults to None.

    Returns:
        class: github.Organization.Organization represents Organizations
    """
   
    g = Github(token)
    org = g.get_organization(organisation)

    return org


