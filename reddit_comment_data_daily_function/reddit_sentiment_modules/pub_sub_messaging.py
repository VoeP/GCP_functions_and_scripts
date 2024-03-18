from google.cloud import pubsub_v1


def publish_success_message(success_message):
    project_id = 'ml-deployments-practice'
    topic_name = 'daily_reddit_api_data_arrival'

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    # Data to be published to the Pub/Sub topic (can be any string)

    # Publish the message to the Pub/Sub topic
    future = publisher.publish(topic_path, data=success_message.encode())
    future.result()  # Wait for the publish operation to complete