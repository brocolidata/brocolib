import json
import os
import pathlib
import pytest
from ..brocolib_extract_load import goblet_utils
import base64

@pytest.fixture
def schedules_list():
    return [
        {
            "cron_schedule":"0 22 * * 1",
            "httpMethod":"POST",
            "name":"freight Casablanca",
            "body": {
                "partition_keys": {"year":"","month":"","lane_code":"china_med_fbx13"},
                "stage_external_table":True,
                "url":"https://fbx.freightos.com/api/lane/{LANE_CODE}?isDaily=false",
                "bucket_file":"freightprices_casablanca",
                "bucket_table_directory":"freight_prices",
                "bucket_directory":"macro/freight",
                "source_type":"json",
                "lane_code":"FBX13"
                
            }
        }
    ]

@pytest.fixture
def create_schedule(schedules_list):
    with open('schedules.json', 'w') as f:
        json.dump(schedules_list, f)


def delete_schedule():
    if os.path.exists('schedules.json'):
        os.remove('schedules.json')


@pytest.fixture
def setup_schedule(create_schedule):

    yield None

    delete_schedule()


def test_get_schedules(setup_schedule, schedules_list):
    schedule_file_path = pathlib.Path(os.getcwd(), "schedules.json")
    ls_schedules = goblet_utils.get_schedules(schedule_file_path)

    assert ls_schedules == schedules_list


def test_encode_body(schedules_list):
    body = schedules_list[0]["body"]
    encoded = goblet_utils.encode_body(body)

    assert encoded == base64.b64encode(
        json.dumps(body).encode('utf-8')
    ).decode('ascii')


def test_check_if_key_in_payload(schedules_list):
    body = schedules_list[0]["body"]
    ls_required = ls_required=["url", "bucket_file", "bucket_directory", "lane_code", "stage_external_table"]
    with pytest.raises(ValueError) as excinfo:
        goblet_utils.check_if_key_in_payload(
            payload=None,
            ls_required=ls_required
        )
    assert str(excinfo.value) == "payload can't be None"

    REMOVED_KEY = "url"
    del body[REMOVED_KEY]
    with pytest.raises(ValueError) as excinfo:
        goblet_utils.check_if_key_in_payload(
            payload=body,
            ls_required=ls_required
        )
    assert str(excinfo.value) == f"Missing key : {REMOVED_KEY}"

