from keys import discord_webhook, urls, keywords
from discordwebhook import Discord
from bs4 import BeautifulSoup
import requests

# sites algorithms are imported from sites directory

from sites import jd_sports


def main():
    check_keywords(urls, keywords)


def check_keywords(urls: list, keywords: list):
    product_urls_file = open("product_urls.txt", "r")
    product_urls = product_urls_file.read().split('\n')
    product_urls_file.close()

    for url in urls:
        content = requests.get(url).content
        soup = BeautifulSoup(content, 'html.parser')
        product_parents = soup.find_all('div', class_='product-item-meta')

        for product_children in product_parents:
            product_name = product_children.find('h2', class_='product-item-meta__title').text.strip()
            for keyword in keywords:
                if keyword in product_name:

                    product_id = product_children.find('h2', class_='product-item-meta__title').get('href').split('/')[-1]
                    product_url = f"https://www.jdsports.co.il/products/{product_id}"

                    if product_url not in product_urls:
                        print(f"New product found: {product_name} - {product_url}")
                        product_urls.append(product_url)

                        webhook_send(discord_webhook, "JD Sports", product_name, product_url, scrape_product_price(product_url), "In Stock", [], scrape_product_image(product_url))
                    break

    product_urls_file = open("product_urls.txt", "w")
    for product_url in product_urls:
        product_urls_file.write(product_url + "\n")
    product_urls_file.close()


def scrape_product_price(url: str):
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')
    print(''.join(filter(lambda x: x.isdigit() or x == '.', soup.find('span', class_='price price--large').text)))

    return ''.join(filter(lambda x: x.isdigit() or x == '.', soup.find('span', class_='price price--large').text))


def scrape_product_image(url: str):
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')
    print(soup.find('div', class_='product__media-image-wrapper').find('img').get('src')[2:])
    return soup.find('div', class_='product__media-image-wrapper').find('img').get('src')[2:]


# webhook_send(discord_webhook, "JD Sports", title, link, check_price(link), "In Stock", [], "")
def webhook_send(discord_webhook: str, website_name: str, product_name: str, product_link: str, product_price: str, product_status: str, product_sizes: list, product_image: str):
    discord = Discord(url=discord_webhook)
    # discord.post(content=f"New shoe has been listed on {website_name}")
    discord.post(
        embeds=[
            {
                "author": {
                    "name": website_name,
                    "url": product_link,
                    "icon_url": "https://picsum.photos/24/24",
                },
                "title": "New Shoe Listed!",
                "description": f"New shoe has been listed on {website_name}",
                "fields": [
                    {"name": "Product Name", "value": product_name, "inline": True},
                    {"name": "Price", "value": product_price, "inline": True},
                    {"name": "Status", "value": product_status},
                ],
                "thumbnail": {"url": f"https://{product_image}"},
                "footer": {
                    "text": "Embed Footer",
                    "icon_url": "https://picsum.photos/20/20",
                },
            }
        ],
    )


if __name__ == "__main__":
    main()
