import json
import pathlib

from google.cloud import pubsub_v1

import model_dispatcher
import model_runners
import preprocessors
from deep_moderator_common.common.message_info import MessageInfoForWorker


class MessageConsumer:
    def __init__(
            self,
            project_id: str,
            local_base_path: pathlib.Path,
            remote_base_path: pathlib.PurePosixPath,
            bucket_name: str):
        self.publisher = pubsub_v1.PublisherClient()
        self._bucket_name = bucket_name
        self._project_id = project_id
        self._model_dispatcher = model_dispatcher.ModelDispatcher(
            local_base_path,
            remote_base_path,
            bucket_name
        )

    def new_message_callback(self, message):
        print(f'Callback received message: {message.data}')
        info: MessageInfoForWorker = MessageInfoForWorker.from_json(message.data)

        probability = self._model_dispatcher.get_model(
            info.group_id,
            model_runners.Runners[info.model_kind],
            preprocessors.Preprocessors[info.preprocessor_kind],
            info.get_model_path_as_pathlib()
        ).run(info.text)

        self.publish_processed(info, probability)
        message.ack()
        print(f"Acked: '{info.get_short_info()}'. Probability: {probability}")

    def publish_processed(
            self,
            info: MessageInfoForWorker,
            probability: float
    ):
        topic_path = self.publisher.topic_path(self._project_id, 'add_classified_comment')
        data = {
            'id': info.id,
            'group_id': info.group_id,
            'probability': probability,
        }
        data_json = json.dumps(data, ensure_ascii=False).encode('utf-8')
        _ = self.publisher.publish(topic_path, data=data_json)
        print(f"Published '{data}'.")
