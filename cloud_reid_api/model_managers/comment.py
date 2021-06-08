from enum import Enum

from google.cloud.datastore import Key, Entity
from exceptions import EntityNotFound
from models import Comment


class Rate(Enum):
    POSITIVE = 'positive'
    NEGATIVE = 'negative'
    UNRATED = 'unrated'


class Sort(Enum):
    DATE_ASC = 'date'
    DATE_DESC = '-date'


class CommentManager:
    def __init__(self, db):
        self.db = db

    def get_comments(self, group_id: int, limit: int = None, offset: int = 0,
                     rate: Rate = None, sort: Sort = None) -> [Comment]:
        group_key = self.db.key('Group', group_id)
        query = self.db.query(kind='Comment', ancestor=group_key)

        if rate is not None:
            if rate is Rate.POSITIVE:
                query.add_filter('known_class', '=', 1)
            elif rate is Rate.NEGATIVE:
                query.add_filter('known_class', '=', 0)
            elif rate is Rate.UNRATED:
                query.add_filter('known_class', '=', None)

        if sort is not None:
            query.order = sort.value

        result = query.fetch(limit=limit, offset=offset)
        comments = [Comment(**comment_entity) for comment_entity in result]

        return comments

    def get_comment(self, group_id: int, comment_id: int) -> Comment:
        comment_key = self.db.key('Group', group_id, 'Comment', comment_id)
        comment_entity = self.db.get(comment_key)
        if comment_entity is None:
            raise EntityNotFound(f'Comment with id={comment_id} from group with id={group_id} not found')

        return Comment(**comment_entity)

    def rate_comment(self, group_id: int, comment_id: int, rate: Rate) -> Comment:
        comment_key: Key = self.db.key('Group', group_id, 'Comment', comment_id)
        comment_entity: Entity = self.db.get(comment_key)
        if comment_entity is None:
            raise EntityNotFound(f'Comment with id={comment_id} from group with id={group_id} not found')

        if rate is Rate.POSITIVE:
            comment_entity['known_class'] = 1
        elif rate is Rate.NEGATIVE:
            comment_entity['known_class'] = 0
        elif rate is Rate.UNRATED:
            comment_entity['known_class'] = None

        self.db.put(comment_entity)

        return Comment(**comment_entity)
