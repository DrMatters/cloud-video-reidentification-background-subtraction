from google.cloud import pubsub_v1
from google.api_core.exceptions import AlreadyExists
from classification_result_saver.main import event_handler

project_id = 'ai-moderator'
subscriber = pubsub_v1.SubscriberClient()


def create_subscription(sub_name, topic_name, callback):
    topic_path = subscriber.topic_path(project_id, topic_name)
    subscription_path = subscriber.subscription_path(project_id, sub_name)

    try:
        subscriber.create_subscription(subscription_path, topic_path)
    except AlreadyExists as e:
        print(e)

    return subscriber.subscribe(subscription_path, callback)


def message_handler(data):
    event_handler(data, {})


def main():
    future = create_subscription('add_classified_comment_sub', 'add_classified_comment', message_handler)

    try:
        future.result()
    except KeyboardInterrupt:
        future.cancel()
        print('\nSuccessful shutdown')
    except Exception as ex:
        future.cancel()
        print(ex)


if __name__ == '_main__':
    main()
