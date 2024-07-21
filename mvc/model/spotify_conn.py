import requests
import Acess.secret
import mvc.model.constants as c


class SpotifyConn:
    def __init__(self):
        self.token = requests.post(c.token_url, data=Acess.secret.get_data())
        self.headers = {
            'Authorization': f'Bearer {self.token.json()["access_token"]}',
            'Content-Type': 'application/json'
        }

    def search(self, name, item, limit):
        params = {
            'q': name,
            'type': item,
            'limit': limit
        }

        response = requests.get(c.search_url, headers=self.headers, params=params)
        data = response.json()
        return data.get(item + 's', {}).get('items', [])

    def get_item(self, item, item_id, q=True):
        if q:
            return requests.get(c.get_url.format(item, item_id), headers=self.headers).json().get(
                'items', [])
        return requests.get(c.get_url.format(item, item_id), headers=self.headers).json()

    def get_items(self, item, item_id, item2, groups=None):
        params = {}
        if groups is not None:
            params['include_groups'] = groups

        return requests.get(c.get_specif_url.format(item, item_id, item2),
                            headers=self.headers, params=params).json().get('items', [])


