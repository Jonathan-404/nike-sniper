from multiprocessing import Process
from keys import keywords
import time

# sites algorithms
from sites.jd_sports import jd_sports
from sites.terminal_x import terminal_x
from sites.factory_54 import factory_54

# sites urls
jd_sports_urls = ["https://www.jdsports.co.il/collections/men-shoes-sneakers?page=", "https://www.jdsports.co.il/collections/women-shoes-sneakers?page="]
terminal_x_url = "https://www.terminalx.com/men/shoes/sneakers-shoes?p="
factory_54_urls = ["https://www.factory54.co.il/men-shoes-sneakers?start="]


def main():

    while True:
        jd_sports_process = Process(target=jd_sports.new_product_urls, args=(jd_sports_urls, keywords))
        jd_sports_process.start()

        terminal_x_process = Process(target=terminal_x.new_product_urls, args=(terminal_x_url, keywords))
        terminal_x_process.start()

        factory_54_process = Process(target=terminal_x.new_product_urls, args=(terminal_x_url, keywords))
        factory_54_process.start()

        time.sleep(30)


if __name__ == "__main__":
    main()
