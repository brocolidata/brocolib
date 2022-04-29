import os
import time
from github import Github
from git import Repo
from cookiecutter.main import cookiecutter
from typing import Union
from brocolib_factory_utils.cookiecutter_utils.cookiecut_utils import *


def create_gith_repo(client_github_token: str,
    organisation: str,
    client_repo: str
):
    org = gith_connect(client_github_token, organisation)
    org.create_repo(client_repo, private=True)

    print('Created new github repo')


def clone_locally(client_github_token,
    organisation,
    client_repo,
    local_dir
):
    new_repo_url = f"https://{client_github_token}@github.com/{organisation}/{client_repo}.git"
    Repo.clone_from(new_repo_url, local_dir)

    print(f'Repo cloned successfully')


def add_gh_secret(
    client_github_token: str,
    organisation: str,
    client_repo: str,
    secr_dict: dict,
):
    """
    function that adds github secrets

    Args:
        token (Union[None , str], optional): Client GitHub token. Defaults to None.
        organisation (Union[None , str]): organisation (or user) name. Defaults to None.
    """
    org = gith_connect(client_github_token, organisation)
    repo_obj = org.get_repo(client_repo)
    if secr_dict:
        counter = 0
        for key, value in secr_dict.items():
            repo_obj.create_secret(key, value)
            counter += 1
            time.sleep(5)
        print(f'{counter} Secrets added successfully')


def cookiec_from_temp(
    templ_repo: str,
    local_dir: str,
    source_token: str,
    source_organisation: str,
    jason_dict: dict,
    directory_name: Union[None, str] = None,
):
    """
    cookiecut repo from given template repo or repo directory

    Args:
        templ_repo (Union[None, str]): GitHub repo that contains the cookiecutter template.
        local_dir (Union[None, str]): local path to spawn the targeted directory/project. Defaults to None.
        source_token (Union[None, str]): GitHub token of Brocoli to access the cookicutter template. Defaults to None.
        source_organisation (Union[None, str]): organisation (or user) name of Brocoli to access the cookicutter template. Defaults to None.
        directory_name (Union[None, str]): targeted directory/project in the templates repo. Defaults to None.
        jason_dict (Union[None, dict], optional): dict of cookiecutt template variables. Defaults to None.
    """

    cookiecut_tmp_url = f"https://{source_token}@github.com/{source_organisation}/{templ_repo}.git"

    if jason_dict:

        if directory_name:

            os.chdir(local_dir)
            cookiecutter(cookiecut_tmp_url, no_input=True,
                         extra_context=jason_dict, directory=directory_name)
        else:
            os.chdir(local_dir)
            cookiecutter(cookiecut_tmp_url, no_input=True,
                         extra_context=jason_dict)

    else:

        if directory_name:

            cookiecutter(cookiecut_tmp_url, no_input=True,
                         directory=directory_name)
        else:
            cookiecutter(cookiecut_tmp_url, no_input=True)
    print("Cookiecut done successfully")

def add_commit_push_all(local_dir: str, message: str):
    os.chdir(local_dir)

    repo = Repo()
    repo.git.add(all=True)

    repo.index.commit(message)
    repo.remotes.origin.push()
    print("Pushed successfully") 
