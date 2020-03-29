import random
from rule34 import Rule34

class _Rule34(object):
    def __init__(self, event_loop):
        self.event_loop = event_loop

    async def get_url_images(self, term):
        rule = Rule34(self.event_loop)
        try:
            images = await rule.getImageURLS(term)
            index = random.randint(0, len(images))
            return images[index]
        except:
            return "Nenhuma imagem encontrada"