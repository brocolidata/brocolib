import argparse
import os
from cookiecutter_utils import cookiecut_template


# Create the parser
my_parser = argparse.ArgumentParser(prog='cookie', description='Cookiecuts repo or repo directory template')


my_parser.add_argument(dest='cookiecut',
                       metavar='Cookiecut',
                       type=str,
                       help='Cookiecuts template from Github directory or repo'
                       )



my_parser.add_argument('-getenvkeys', '--environmentkeys', help='delimited list input to look for in env and pass to cookiecut', type=str)

# Execute the parse_args() method
my_parser.add_argument('-setsecrets', '--secretkeys', help='delimited list input to look for in env and pass to cookiecut', type=str)






args = my_parser.parse_args()

cookiecut_temp_repo = args.cookiecut

# creating repo and cloning locally
cookiecut_template.create_gith_repo()

cookiecut_template.clone_locally()




# adding env variables to dict and checking for environment variables
env_variables = args.envkeys

env_list = [str(item) for item in env_variables.split(',')]

env_variables_dic = {}

if env_variables:

    for key_elem in env_list:
        for c in [":","="]:
            if c in key_elem:
                env_k, env_v= key_elem.split(c)
                if env_k not in env_variables_dic:
                    os.environ[env_k.upper()] = env_v

                    env_variables_dic[env_k.upper()] = os.getenv(env_k.upper())
                else:
                    raise ValueError(f'environment variable {env_k} given twice')

            else: 
                if key_elem not in env_variables_dic:
                    val = os.getenv(key_elem.upper())
                    env_variables_dic[key_elem.upper()] = val
                else:
                    raise ValueError(f'environment variable {key_elem} given twice')
    cookiecut_template.cookiec_from_temp(templ_repo=cookiecut_temp_repo, jason_dict=env_variables_dic)
else:
    cookiecut_template.cookiec_from_temp(templ_repo=cookiecut_temp_repo)
    


# adding secrets to dict

secrets = args.secretkeys

secrets_list = [str(item) for item in secrets.split(',')]

secrets_dic = {}

if secrets:

    for key_elem in secrets_list:
        for c in [":","="]:
            if c in key_elem:
                secr_k, secr_v= key_elem.split(c)
                if secr_k not in secrets_dic:
                    os.environ[secr_k.upper()] = secr_v
                    secrets_dic[secr_k.upper()] = os.getenv(secr_k.upper())
                else:
                    raise ValueError(f'secret key {secr_k} given twice')
            else:    
                if key_elem not in secrets_dic:
                    val = os.getenv(key_elem.upper())
                    secrets_dic[key_elem.upper()] = val
                
    
    cookiecut_template.add_gh_secret(secr_dict=secrets_dic)


print('Cookiecutting Template Successful')

