from google.cloud import pubsub
import json


def publish_message_toPubSub(project_id, topic_id, message, logger):

    publisher = pubsub.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    future = publisher.publish(topic_path, message)
    if logger:
        logger.info(future.result())
    
    return future.result()


def publish_message(sources, dbt_topic, gcp_project, logger=None):
    message = {"sources":sources}
    publish_message_toPubSub(
        project_id=gcp_project,
        topic_id=dbt_topic,
        message=json.dumps(message).encode("utf-8"),
        logger=logger
    )