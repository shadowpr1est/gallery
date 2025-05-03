from gallery.settings import PEXELS_API_KEY
import requests
class PexelsAPI:
    def __init__(self):
        self.api_key = PEXELS_API_KEY
        self.base_url = 'https://api.pexels.com/v1/'
    def get_photo(self, query, per_page=10):
        headers = {'Authorization' : self.api_key}
        params = {
            'query':query,
            'per_page':per_page
        }
        response = requests.get(self.base_url + 'search', headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            print(data)
            return [photo['src']['original'] for photo in data['photos']]
        else:
            print(f"Failed to fetch the images: {response.status_code}")
            return []
