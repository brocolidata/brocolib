from google.cloud import pubsub_v1

def publish_message_toPubSub(project_id, topic_id, message, logger):

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    future = publisher.publish(topic_path, message)
    if logger:
        logger.info(future.result())
    
    return future.result()