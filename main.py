from keys import keywords
import time

# sites algorithms
from sites.jd_sports import jd_sports

# sites urls
jd_sports_url = "https://www.jdsports.co.il/collections/men-shoes-sneakers?page="


def main():
    while True:
        jd_sports.new_product_urls(jd_sports_url, keywords)
        time.sleep(30)


if __name__ == "__main__":
    main()
