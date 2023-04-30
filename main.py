from keys import discord_webhook
from discordwebhook import Discord
from bs4 import BeautifulSoup
import requests
import time


urls = ['']
keywords = ['']


def main():
    webhook_send(discord_webhook, "Hello World!")


def check_price(urls: list):
    pass


def webhook_send(discord_webhook: str, message: str):
    webhook = Discord(url=discord_webhook)

    webhook.post(
        embeds=[
            {
                "author": {
                    "name": "Shoes Website",
                    "url": "https://shoes.com/",
                    "icon_url": "https://shoes.com/",
                },
                "title": "NEW SHOE!",
                "description": "New shoe has been released on the website!",
                "fields": [
                    {"name": "Price", "value": "999.0 ILS", "inline": True},
                    {"name": "Status", "value": "In Stock", "inline": True},
                    {"name": "Available Sizes", "value": "99, 99, 99", "inline": False},
                ],
                "thumbnail": {"url": "https://picsum.photos/80/60"},
                "image": {"url": "https://picsum.photos/400/300"},
                "footer": {
                    "text": "Embed Footer",
                    "icon_url": "Rights Reserved to Jonathan & Liam",
                },
            }
        ],
    )


if __name__ == "__main__":
    main()
