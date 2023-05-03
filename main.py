from keys import keywords
import time

# sites algorithms
from sites.jd_sports import jd_sports

# sites urls
jd_sports_url = "https://www.jdsports.co.il/collections/men-shoes-sneakers?page="


def main():
    while True:
        start = time.time()
        jd_sports.new_product_urls(jd_sports_url, keywords)
        end = time.time()
        print(f"Time taken: {end - start} seconds")
        # time.sleep(60)


if __name__ == "__main__":
    main()
