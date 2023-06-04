from bs4 import BeautifulSoup
import requests

from .scrape_functions import get_price, get_image, get_sizes
from ..utils import get_urls
from ..Shoe import Shoe

""" TERMINAL X """

def get(url: str):
    for i in range(17):

        """change it to a utils function that returns a list of urls"""
        urls = get_urls()

        content = requests.get(f"{url}{i+1}").content
        soup = BeautifulSoup(content, 'html.parser')
        product_parents = soup.find_all('div', class_='img-link_29yX new-listing-product_2S9n')

        for product_children in product_parents:
            name = product_children.get('title')
            product_url = f"https://www.terminalx.com/men/shoes/sneakers-shoes{product_children.find('a').get('href')}"

            sec_content = requests.get(product_url).content
            sec_soup = BeautifulSoup(sec_content, 'html.parser')
            price = get_price(sec_soup).strip()
            sizes = get_sizes(sec_soup)
            image = get_image(sec_soup).strip()

            shoe = Shoe("terminal_x", name, product_url, price, image, sizes)

            if product_url not in urls:

                shoe.discord_message()
                shoe.update()
                urls.append(product_url)
