import logging
from brocolib_utils.data_studio import DataStudio


def update_exposures(data: dict):
    for element in data["exposures"]:
        exposure_title = element["name"]
        exposure_meta_dict = element["meta"]
        asset_id = exposure_meta_dict.get("asset_id")
        grants_dict = exposure_meta_dict.get("grants")

        if grants_dict:
            client = DataStudio()
            permissions = client.get_permissions(asset_id=asset_id)
            
            if permissions["response"] != 200:
                logging.error(permissions["response"])
            elif permissions["response"]["permissions"] != grants_dict:
                permissions_updated = client.update_permissions(
                    asset_id=asset_id,
                    permission_dict={"permissions":grants_dict}
                )
                if permissions_updated["response"] != 200:
                    logging.error(permissions_updated["response"])
                else:
                    logging.info(f"Permissions for {exposure_title} have been updated successfully !")
            else:
                logging.info(f"No changes in permissions detected for {exposure_title}")

    logging.info('DONE')

    
