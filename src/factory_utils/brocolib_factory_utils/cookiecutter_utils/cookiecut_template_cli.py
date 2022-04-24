import argparse
import os
import cookiecut_template


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

    for key in env_list:

        if key not in env_variables_dic:
            val = os.getenv(key)
            env_variables_dic[key.lower()] = val
    cookiecut_template.cookiec_from_temp(templ_repo=cookiecut_temp_repo, jason_dict=env_variables_dic)
else:
    cookiecut_template.cookiec_from_temp(templ_repo=cookiecut_temp_repo)
    


# adding secrets to dict

secrets = args.secretkeys

secrets_list = [str(item) for item in secrets.split(',')]

secrets_dic = {}

if secrets:

    for key in secrets_list:

        if key not in secrets_dic:
            val = os.getenv(key)
            secrets_dic[key.lower()] = val
    
    cookiecut_template.add_gh_secret(secr_dict=secrets_dic)


print('Cookiecutting Template Successful')

