import requests

headers = {
    "Host": "www.adidas.co.il:443",
    "Proxy-Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}


r = requests.get("https://www.adidas.co.il/he/men-sneakers", headers=headers).content
print(r)