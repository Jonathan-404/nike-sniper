import json

def get_urls():
    urls = []

    product_data_file = json.load(open("./product_data.json", "r"))
    for product in product_data_file["terminal_x"]:
        urls.append(product["url"])

    return urls
