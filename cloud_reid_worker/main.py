import pathlib
import tempfile
from argparse import ArgumentParser
from typing import Callable

from google.api_core.exceptions import AlreadyExists
from google.cloud import pubsub_v1

import message_consumer
import vars

subscriber = pubsub_v1.SubscriberClient()


def create_subscription(project_id: str, sub_name: str, topic_name: str):
    subscription_path = subscriber.subscription_path(project_id, sub_name)
    topic_path = subscriber.topic_path(project_id, topic_name)

    try:
        subscriber.create_subscription(subscription_path, topic_path)
    except AlreadyExists as e:
        print(e)


def subscribe(project_id: str, sub_name: str, callback: Callable[[str], None]):
    subscription_path = subscriber.subscription_path(project_id, sub_name)

    print("Subscribing to callback")
    return subscriber.subscribe(subscription_path, callback)


def main():
    parser = ArgumentParser()
    parser.add_argument('--create-sub', type=bool, default=False, help='create subscription')
    args = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix=vars.dir_prefix) as temp_dir:
        path_base_temp_dir = pathlib.Path(temp_dir)
        if not path_base_temp_dir.exists():
            raise FileNotFoundError('Temporary directory not generated')

        consumer = message_consumer.MessageConsumer(
            project_id=vars.project_id,
            local_base_path=path_base_temp_dir,
            remote_base_path=pathlib.PurePosixPath(vars.remote_base_path),
            bucket_name=vars.bucket_name)

        if args.create_sub:
            create_subscription(vars.project_id, vars.sub_name, vars.topic_name)

        future = subscribe(vars.project_id, vars.sub_name, consumer.new_message_callback)
        try:
            future.result()
        except KeyboardInterrupt:
            future.cancel()
            print('\nSuccessful shutdown')
        except Exception as ex:
            future.cancel()
            print(ex)


if __name__ == "__main__":
    main()
