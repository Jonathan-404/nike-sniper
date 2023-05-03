from keys import keywords
import time

# sites algorithms
from sites.jd_sports import jd_sports
from sites.foot_locker import foot_locker

# sites urls
jd_sports_url = "https://www.jdsports.co.il/collections/men-shoes-sneakers?page="
foot_locker_url = "https://www.footlocker.co.il/men/%D7%A0%D7%A2%D7%9C%D7%99%D7%99%D7%9D/%D7%A1%D7%A0%D7%99%D7%A7%D7%A8%D7%A1/cat?category_id=60dc6b043191a1000854a462"


def main():
    while True:
        jd_sports.new_product_urls(jd_sports_url, keywords)
        foot_locker.new_product_urls(foot_locker_url, keywords)
        time.sleep(30)


if __name__ == "__main__":
    main()
