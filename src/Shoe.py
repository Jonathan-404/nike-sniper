import json
from webhook_manager import new_shoe_message

class Shoe:
    def __init__(self, site, name, url, price, img, sizes):
        self.site = site
        self.name = name
        self.url = url
        self.img = img
        self.price = price
        self.sizes = sizes

    def json(self):
        return {
            "name": self.name,
            "url": self.url,
            "img": self.img,
            "price": self.price,
            "sizes": self.sizes,
            "stock": "In Stock"
        }

    def discord_message(self):
        new_shoe_message(self.site, self.name, self.url, self.price, "In Stock", self.sizes, self.img)

    def update(self):
        with open("product_data.json", 'r+') as file:
            file_data = json.load(file)
            file_data[self.site].append(self.json())
            file.seek(0)
            json.dump(file_data, file, indent=4)


