import uuid
from together import Together
import requests
from django.core.cache import cache
from gallery.settings import PEXELS_API_KEY


class PexelsAPI:
    _cached_generated_images = None

    def __init__(self):
        self.api_key = PEXELS_API_KEY
        self.base_url = 'https://api.pexels.com/v1/'

    def get_photo(self, query, per_page=10):
        cache_key = f"pexels:{query}:{per_page}"
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result

        headers = {'Authorization': self.api_key}
        params = {'query': query, 'per_page': per_page}
        response = requests.get(self.base_url + 'search', headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            images = [
                {
                    "id": str(uuid.uuid4()),
                    "data": photo['src']['original']
                } for photo in data['photos']
            ]

            cache.set(cache_key, images, timeout=60 * 60)
            for img in images:
                cache.set(f"image:{img['id']}", img, timeout=60 * 60)

            return images
        else:
            print(f"Failed to fetch the images: {response.status_code}")
            return []

    def generated_photo(self, query):
        cache_key = f"generated:{query}"
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result

        client = Together()
        response = client.images.generate(
            prompt=query,
            model="black-forest-labs/FLUX.1-schnell-Free",
            width=512,
            height=512,
            steps=1,
            n=1,
            response_format="b64_json",
            stop=[]
        )

        images = []
        for item in response.data:
            img_data = f"data:image/png;base64,{item.b64_json}"
            image_obj = {
                "id": str(uuid.uuid4()),
                "data": img_data
            }
            images.append(image_obj)
            cache.set(f"image:{image_obj['id']}", image_obj, timeout=60 * 60)

        cache.set(cache_key, images, timeout=60 * 60)
        return images

    def get_cached_generated_images(self):
        cache_key = "cached_generated_images"
        cached_images = cache.get(cache_key)
        if cached_images is not None:
            return cached_images

        images = (
            self.generated_photo("Elephant") +
            self.generated_photo("Zebra") +
            self.generated_photo("Monkey") +
            self.generated_photo("Bird") +
            self.generated_photo("Giraffe")
        )

        cache.set(cache_key, images, timeout=60 * 60)
        for img in images:
            cache.set(f"image:{img['id']}", img, timeout=60 * 60)

        return images
