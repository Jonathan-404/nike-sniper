from discordwebhook import Discord
from keys import discord_webhook


"""
THIS IS THE WEBHOOK MANAGER FILE

"""


def new_shoe_message(website_name: str, product_name: str, product_link: str, product_price: str, product_status: str, product_sizes: list, product_image: str):
    discord = Discord(url=discord_webhook)
    discord.post(
        embeds=[
            {
                "color": 0x00ff00,
                "type": "rich",
                "url": product_link,
                "author": {
                    "name": website_name,
                    "url": product_link,
                },
                "title": "New Shoe Listed!",
                "description": f"New shoe has been listed on {website_name}",
                "fields": [
                    {"name": "Product Name", "value": product_name, "inline": True},
                    {"name": "Price", "value": f"{product_price} ILS", "inline": True},
                    {"name": "Status", "value": product_status},
                    {"name": "Sizes", "value": f"{' '.join(product_sizes)}"},
                ],
                "thumbnail": {"url": f"https://{product_image}"},
                "footer": {
                    "text": "All rights reserved to @Joe#6715 and @0rphan#6372",
                },
            }
        ],
    )
