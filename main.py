from keys import keywords

# sites algorithms
from sites.jd_sports import jd_sports

# sites urls
jd_sports_url = "https://www.jdsports.co.il/collections/men-shoes-sneakers"


def main():
    while True:
        jd_sports.new_product_urls(jd_sports_url, keywords)


if __name__ == "__main__":
    main()
