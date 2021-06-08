from google.cloud.datastore import Key, Entity

from exceptions import EntityNotFound


class GroupManager:
    def __init__(self, db):
        self.db = db

    def get_groups(self):
        query = self.db.query(kind='Group')
        result = query.fetch()
        groups = [{'id': group_entity.id} for group_entity in result]

        return groups

    def get_group(self, group_id: int):
        group_key: Key = self.db.key('Group', group_id)
        group_entity: Entity = self.db.get(group_key)
        if group_entity is None:
            raise EntityNotFound()

        group_entity['id'] = group_entity.id

        return group_entity
