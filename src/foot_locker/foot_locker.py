# from sites.foot_locker.scarpe_functions import scrape_product_price, scrape_product_image, scrape_product_sizes
from webhook_manager import new_shoe_message
from bs4 import BeautifulSoup
import requests
import json

"""
SITE ALGORITHM STARTS HERE

SITE NAME: Foot Locker
"""

#
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "max-age=0",
    "cookie": "_gcl_au=1.1.774905418.1683127359; glassix-visitor-id-v2-44f1f8a2-a1a8-4b38-bdfc-8cd8cb881b20=0ece813f-1e03-4604-9499-1226c5ba58ac; _fbp=fb.2.1683127360567.381991064; _hjDonePolls=889094; _hjSessionUser_3393939=eyJpZCI6IjFhNTdmZDI0LTJjYjUtNTljYi1hNmE5LWIzZjRjMDk3Y2RlZCIsImNyZWF0ZWQiOjE2ODMxMjczNjAxOTksImV4aXN0aW5nIjp0cnVlfQ==; _gid=GA1.3.1209728225.1683354004; _hjIncludedInSessionSample_3393939=1; _hjSession_3393939=eyJpZCI6ImQ0ODhkMjQ3LTlhYzEtNGUxMC05NmZiLTI3ZGM4MzdkYzk2MiIsImNyZWF0ZWQiOjE2ODMzNTQwMDg2MTYsImluU2FtcGxlIjp0cnVlfQ==; _hjAbsoluteSessionInProgress=0; __za_cds_19763555=%7B%22data_for_campaign%22%3A%7B%22country%22%3A%22IL%22%2C%22language%22%3A%22UNSET%22%2C%22ip%22%3A%22109.66.156.55%22%2C%22start_time%22%3A1683354277000%2C%22session_groups%22%3A%7B%223237%22%3A%7B%22campaign_Id%22%3A%2280889%22%7D%2C%223238%22%3A%7B%22campaign_Id%22%3A%2280890%22%7D%7D%7D%7D; __za_19763555=%7B%22sId%22%3A6310020%2C%22dbwId%22%3A%221%22%2C%22sCode%22%3A%222a1d26236fed8a57d2f618ef812f5a8b%22%2C%22sInt%22%3A5000%2C%22na%22%3A2%2C%22td%22%3A1%2C%22ca%22%3A%221%22%7D; _ga=GA1.3.1424194023.1683127359; _gat_gtag_UA_197949286_1=1; _gat_UA-197949286-1=1; _immue=DMRzfJDHE4VNV3pxxQWbHW2pQOvyHYOBvP6sRlqwOXQQqIrAcffqAd6ND6LrdB%2FCtJ%2FY9mybRPEY7JUQLPZ8HdyAomrQA0S8eEeidLf9M%2FpsnQGdD%2BfrqR%2F0L27s8m1ZyJLvO9s4rVF%2F0R9tz3O3vuHiMgKH8v%2BZWYPO8qxYMtdgWqtuyXER9hFFRyqkGgtbJCw9rgdLFOcZ5yuvWoLJCQ%2BfHWBFVUaWMlBXRWxOTNh2%2FLmOrIO9Hro%2Fzl9IC8KWn47Idsmfq4pf%2B5xNvenFYFJHlFUhatLyyrE1xoQlnKutk%2FSmQ3gQm0T2eUc7fuTiOk1rYIudCFV1o0xNaC1Ta83TjtPZjHJ2VSBcRwW9sYesURPFNpx%2FnidxCJLW560DbnM4P%2BFguIL5A3vYxP%2BHof5hwzH0DGlsK3taXfDMxVpdlr2wAEe4jIyibJtWntmGWFuMxx46IlGkiU9qOfWgDHneZ5loSR1z%2FPDsQdMyE7M%3D; __za_cd_19763555=%7B%22visits%22%3A%22%5B1683354283%2C1683127361%5D%22%2C%22campaigns_status%22%3A%7B%2274959%22%3A1683354707%2C%2278311%22%3A1683354707%2C%2281114%22%3A1683128651%7D%7D; _ga_SLEJV4R8K1=GS1.1.1683354003.4.1.1683354708.58.0.0",
    "sec-ch-ua": r"\"Google Chrome\";v=\"89\", \"Chromium\";v=\"89\", \";Not A Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "macOS",
    "sec-fetch-dest": "document",
    "sec-fetch-site": "same-origin",
    "sec-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
}


res = requests.get("https://www.footlocker.co.il/men/cat?category_id=60dc6b043191a1000854a462&limit=300&offset=16", headers=headers).content
print(res)


def new_product_urls(url: str, keywords: list):
    pass


def update_products_json_file(company_name: str, product_data: dict):
    with open("data.json", 'r+') as file:
        file_data = json.load(file)
        file_data[company_name].append(product_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)
