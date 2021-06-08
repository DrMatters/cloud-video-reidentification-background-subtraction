import os
import typing
from enum import Enum

import deep_moderator_common.common.message_info as common
import flask
from google.cloud import datastore, pubsub_v1

project_id = os.environ['GCP_PROJECT']

datastore_client: typing.Union[datastore.Client, None] = None
publisher: typing.Union[pubsub_v1.PublisherClient, None] = None


class DeletedBy(Enum):
    AI = 'ai'
    MODERATOR = 'moderator'
    USER = 'user'


def event_handler(request: flask.Request):
    content = request.get_json()
    event_type = content['type']
    group_id = content['group_id']

    if event_type == 'confirmation':
        return get_group_key(group_id)

    comment = content['object']

    if event_type == 'wall_reply_new':
        handle_wall_reply_new(group_id, comment)
        return 'ok'

    if event_type == 'wall_reply_delete':
        handle_wall_reply_delete(group_id, comment)
        return 'ok'

    if event_type == 'wall_reply_edit':
        handle_wall_reply_edit(group_id, comment)
        return 'ok'

    if event_type == 'wall_reply_restore':
        handle_wall_reply_restore(group_id, comment)
        return 'ok'

    flask.abort(400)


def handle_wall_reply_new(group_id: int, comment):
    add_comment(group_id, comment)
    push_comment_to_queue(group_id, comment)


def handle_wall_reply_delete(group_id: int, delete_resp_body):
    set_comment_deleted(group_id, **delete_resp_body)


def handle_wall_reply_edit(group_id, comment):
    edit_comment(group_id, comment['id'], comment['text'])
    push_comment_to_queue(group_id, comment)


def handle_wall_reply_restore(group_id, comment):
    restore_comment(group_id, comment['id'])


def add_comment(group_id, comment):
    global datastore_client
    if not datastore_client:
        datastore_client = datastore.Client()

    comment_key = datastore_client.key('Group', group_id, 'Comment', comment['id'])
    comment_entity = datastore.Entity(key=comment_key)

    comment_entity.update(comment)
    comment_entity.update({
        'group_id': group_id,
        'known_class': None,  # None stands for unknown
        'predicted_probability': None,  # None stands for unpredicted
    })

    datastore_client.put(comment_entity)


def set_comment_deleted(group_id, comment_id, deleter_id, owner_id):
    global datastore_client
    if not datastore_client:
        datastore_client = datastore.Client()

    comment_key = datastore_client.key('Group', group_id, 'Comment', comment_id)
    comment_entity = datastore_client.get(comment_key)

    if 'deleted_by' in comment_entity and comment_entity['deleted_by'] == DeletedBy.AI:
        return

    if deleter_id != comment_entity['from_id']:
        comment_entity['known_class'] = 1
        comment_entity['deleted_by'] = DeletedBy.MODERATOR
    else:
        comment_entity['deleted_by'] = DeletedBy.USER

    comment_entity.update(owner_id=owner_id, deleter_id=deleter_id)

    datastore_client.put(comment_entity)


def restore_comment(group_id, comment_id):
    global datastore_client
    if not datastore_client:
        datastore_client = datastore.Client()

    comment_key = datastore_client.key('Group', group_id, 'Comment', comment_id)
    comment_entity = datastore_client.get(comment_key)

    comment_entity.pop('deleter_id', None)

    datastore_client.put(comment_entity)


def edit_comment(group_id, comment_id, new_text):
    global datastore_client
    if not datastore_client:
        datastore_client = datastore.Client()

    comment_key = datastore_client.key('Group', group_id, 'Comment', comment_id)
    comment_entity = datastore_client.get(comment_key)

    comment_entity.update(text=new_text)

    datastore_client.put(comment_entity)


def push_comment_to_queue(group_id: int, comment):
    global publisher
    if not publisher:
        publisher = pubsub_v1.PublisherClient()

    group_key = datastore_client.key('Group', group_id)
    group_entity = datastore_client.get(group_key)

    message_for_worker = common.MessageInfoForWorker(
        id=comment['id'],
        group_id=group_id,
        text=comment['text'],
        model_path=group_entity['model_path'],
        model_kind=group_entity['model_kind'],
        preprocessor_kind=group_entity['preprocessor_kind']
    )
    data = message_for_worker.json().encode('utf-8')

    topic_path = publisher.topic_path(project_id, 'new_comment')
    future = publisher.publish(topic_path, data=data)
    print(f'Published {data.decode("utf-8")} of message ID {future.result()}.')


def get_group_key(group_id: int) -> str:
    global datastore_client
    if not datastore_client:
        datastore_client = datastore.Client()

    group_key = datastore_client.key('Group', group_id)
    group_entity = datastore_client.get(group_key)

    return group_entity['confirmation_key']
