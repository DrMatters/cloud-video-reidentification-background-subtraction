from aiohttp import ClientSession


class VKAPI:
    VERSION = '5.101'
    BASE_URL = 'https://api.vk.com/method'
    GET_GROUPS_URL = f'{BASE_URL}/groups.getById'

    def __init__(self, key):
        self.key = key

    async def get_groups_by_id(self, *group_ids: int):
        params = {
            'access_token': self.key,
            'v': self.VERSION,
            'group_ids': ','.join(str(group_id) for group_id in group_ids),
        }

        async with ClientSession() as session:
            async with session.get(self.GET_GROUPS_URL, params=params) as response:
                response_object = await response.json()

                return response_object['response']
