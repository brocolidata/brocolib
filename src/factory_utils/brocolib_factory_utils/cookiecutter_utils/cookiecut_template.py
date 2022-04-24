import os
import time
from github import Github
from git import Repo
from cookiecutter.main import cookiecutter
from typing import Union
from cookiecut_utils import * 


def create_gith_repo():
    org = gith_connect()
    org.create_repo(new_repo, private=True)


def clone_locally():
    new_repo_url = f"https://{client_gh_token}@github.com/{client_org}/{new_repo}.git"
    Repo.clone_from(new_repo_url, local_path)

def add_gh_secret( 
    secr_dict: Union[None , dict],
    repo: Union[None , str] = new_repo,
):
    """
    function that adds github secrets

    Args:
        token (Union[None , str], optional): Client GitHub token. Defaults to None.
        organisation (Union[None , str]): organisation (or user) name. Defaults to None.
    """

    org = gith_connect()
    repo= repo or new_repo

    if repo is None:
        raise ValueError('repo variable must be set or given')

    repo_obj = org.get_repo(repo)
    if secr_dict:
        counter = 0
        for key, value in secr_dict.items():
            repo_obj.create_secret(key,value)
            counter += 1
            time.sleep(5)
            print(f'Done {counter}')

        


def cookiec_from_temp(
    templ_repo: Union[None, str]= broc_temp_repo,
    local_dir: Union[None, str] = local_path,
    source_token: Union[None, str] = broc_gh_token,
    source_organisation: Union[None, str] = broc_org,
    directory_name: Union[None, str] = None,
    jason_dict: Union[None, dict] = None,
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
    for x in [templ_repo, local_dir, source_token, source_organisation]:
        if x is None:
            raise ValueError(f'{x} variable must be set or given')


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

