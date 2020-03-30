import requests
import io

class Tools(object):
    def image_to_bytes(self, image):
        with requests.get(image) as url:
            return io.BytesIO(url.content)