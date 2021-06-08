from datetime import datetime
from google.cloud import datastore

datastore_client = None


def event_collector(request):
    global datastore_client
    if not datastore_client:
        datastore_client = datastore.Client()

    content = request.get_json()
    event_type = content['type']
    group_id = content['group_id']
    secret = content['secret']

    if not verify_group_secret(group_id, secret):
        return 'error'

    if event_type == 'confirmation':
        return get_group_key(group_id)

    comment = content['object']

    event_key = datastore_client.key('Event')
    event_entity = datastore.Entity(event_key)
    event_entity.update(group_id=group_id, event_type=event_type, collection_date=datetime.now(), **comment)

    datastore_client.put(event_entity)

    return 'ok'


def get_group_key(group_id: int) -> str:
    global datastore_client
    if not datastore_client:
        datastore_client = datastore.Client()

    group_key = datastore_client.key('Group', group_id)
    group_entity = datastore_client.get(group_key)

    return group_entity['confirmation_key']


def verify_group_secret(group_id: int, secret: str):
    global datastore_client
    if not datastore_client:
        datastore_client = datastore.Client()

    group_key = datastore_client.key('Group', group_id)
    group_entity = datastore_client.get(group_key)

    return group_entity['secret'] == secret
