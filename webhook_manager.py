from discordwebhook import Discord
from keys import discord_webhook


"""
THIS IS THE WEBHOOK MANAGER FILE

"""


def webhook_send(website_name: str, product_name: str, product_link: str, product_price: str, product_status: str, product_sizes: list, product_image: str):
    discord = Discord(url=discord_webhook)

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
                    {"name": "Price", "value": f"{product_price} ILS", "inline": True},
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
