import json
import requests
from brocolib_utils import credentials
from brocolib_utils.settings import (DATA_STUDIO_API_BASE_URL, DATA_STUDIO_ASSETS_TYPES, 
    DATA_STUDIO_API_SCOPE)


def response_helper(**kwargs) -> dict:
    return {
        "status": kwargs['status'],
        "response":kwargs['response']
    }


class DataStudio:
    # This func runs as default when DataStudio class runs.
    def __init__(self, *args, **kwargs):
        self.headers = credentials.get_jwt_header(DATA_STUDIO_API_SCOPE)

    # def get_assets(self, asset_id, asset_type) -> dict:
    def get_assets(self, asset_type: DATA_STUDIO_ASSETS_TYPES) -> dict:
        r = requests.get(
            url=f"{DATA_STUDIO_API_BASE_URL}/assets:search",
            headers=self.headers,
            params={"assetTypes":[asset_type]}
        )

        if r.status_code == 200:
            return response_helper(status=r.status_code, response=json.loads(r.text))
        else:
            return response_helper(status=r.status_code, response=r.reason)


    def get_asset_by_title(self, asset_type: DATA_STUDIO_ASSETS_TYPES, asset_title: str) -> str:
        assets = self.get_assets(asset_type)
        if assets["status"] == 200: 
            if assets["response"]["assets"]:
                return list(filter(lambda asset: asset["title"] == asset_title, assets["response"]["assets"]))[0]


    def get_asset_by_name(self, asset_type: DATA_STUDIO_ASSETS_TYPES, asset_name: str) -> str:
        assets = self.get_assets(asset_type)
        if assets["status"] == 200: 
            if assets["response"]["assets"]:
                return list(filter(lambda asset: asset["name"] == asset_name, assets["response"]["assets"]))[0]



    def get_permissions(self, asset_id: str) -> dict:
        r = requests.get(f"{DATA_STUDIO_API_BASE_URL}/assets/{asset_id}/permissions",
            headers=self.headers)

        if r.status_code == 200:
            return response_helper(status=r.status_code, response=json.loads(r.text))
        else:
            return response_helper(status=r.status_code, response=r.reason)


    def update_permissions(self, asset_id: str, permission_dict: dict) -> dict:
        data = {
            'permissions': permission_dict
        }
        # data = permission_dict

        r = requests.patch(f"{DATA_STUDIO_API_BASE_URL}/assets/{asset_id}/permissions",
            headers=self.headers,
            json=data)

        if r.status_code == 200:
            return response_helper(status=r.status_code, response=json.loads(r.text))
        else:
            # return response_helper(status=r.status_code, response=r.reason)
            return r


    # def add_member(self, role: str, user_email_array: list) -> dict:
    #     data = {
    #         'name':assetId,
    #         'role': role,
    #         'members': user_email_array
    #     }

    #     r = requests.post(f"{DATA_STUDIO_API_BASE_URL}/assets/{assetId}/permissions:addMembers",
    #         headers=self.headers,
    #         data=data)

    #     if r.status_code == 200:
    #         return response_helper(status=r.status_code, response=json.loads(r.text))
    #     else:
    #         return response_helper(status=r.status_code, response=r.reason)

#     def revoke_permissions(self, user_email_array: list) -> dict:
#         data = {
#             'name':assetId,
#             'members': user_email_array
#         }

#         r = requests.post(f"{DATA_STUDIO_API_BASE_URL}/assets/{assetId}/permissions:revokeAllPermissions",
#             headers=self.headers,
#             data=data)

#         if r.status_code == 200:
#             return response_helper(status=r.status_code, response=json.loads(r.text))
#         else:
#             return response_helper(status=r.status_code, response=r.reason)



## -----| TESTS |-----
# test_user_array = ['group:administrators@brocoli.tech']
# client = DataStudio()
# asset_type = "REPORT"
# # asset_type = "DATA_SOURCE"
# # assets = client.get_assets(asset_type)
# # # print(assets)
# # for element in assets["response"]["assets"]:
# #     print(element["title"])
# #     permissions = client.get_permissions(asset_id=element["name"])
# #     print(permissions)
# #     print('=====')

# asset = client.get_asset_by_title(
#     asset_title="dbt monitoring",
#     asset_type="REPORT"
# )

# asset_id = asset["name"]
# permissions = client.get_permissions(asset_id)
# print(permissions)



# # permission_dict = {'permissions': {'EDITOR': {'members': ['group:administrators@brocoli.tech']}, 'OWNER': {'members': ['user:amirb@brocoli.tech']}}}
# # updated_permissions =  client.update_permissions(asset_id, permission_dict)
# # print(updated_permissions)

# print('hello')