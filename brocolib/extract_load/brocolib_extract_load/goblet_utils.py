import base64
import os
import json

def check_if_key_in_payload(payload, ls_required):
    """[summary]

    Args:
        body (dict): body of the request
        ls_required (list): list of keys required in the body

    Raises:
        ValueError: if payload is None
        ValueError: if key not in payload
    """
    if payload is None:
        raise ValueError("payload can't be None")
    for key in ls_required:
        if key not in payload:
            raise ValueError(f"Missing key : {key}")


def encode_body(body):
    """base64 encode the body that will be POSTed by Cloud Scheduler

    Args:
        body (dict): dict to encode

    Returns:
        bytes: encoded body
    """
    return base64.b64encode(
        json.dumps(body).encode('utf-8')
    ).decode('ascii')


def yad(decoratator_list):
    """Yet Another Decorator
    Loop over a list of decorators and create a unique
    decorator that contains them all.

    Args:
        decoratator_list (list): list of decorators
    """
    def decorator(f):
        for d in reversed(decoratator_list):
            f = d(f)
        return f
    return decorator


def get_schedules(schedule_filepath):
    with open(schedule_filepath) as f:
        LS_SCHEDULES = json.load(f)
    return LS_SCHEDULES


def get_decorator_list(app, schedule_filepath):
    """For every schedule : 
    - Create a decorator for the schedule
    - Add it to a list of decorators

    Args:
        app (goblet.Goblet): Goblet app object
        schedule_filepath (str): path to the schedule json file

    Returns:
        goblet_decoratator_list (list): list of decorators
    """
    goblet_decoratator_list = []
    for schedule in get_schedules(schedule_filepath):
        goblet_decoratator_list.append(
            app.schedule(
                schedule["cron_schedule"], 
                httpMethod=schedule["httpMethod"], 
                headers={"x-cron": schedule["cron_schedule"]}, 
                body=encode_body(schedule["body"]), 
                description=schedule["name"]
            )
        )
    return goblet_decoratator_list


def add_schedules(app, schedule_filepath):
    """Decorator that adds all the schedule
    to a Cloud Function handler

    Args:
        app (goblet.Goblet): goblet app object
        schedule_filepath (str): path to the schedule json file

    Returns:
        yad: decorator containing all the shedules' decorators
    """
    goblet_decoratator_list = get_decorator_list(app, schedule_filepath)
    return yad(goblet_decoratator_list)