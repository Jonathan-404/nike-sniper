from multiprocessing import Process
from keys import keywords
import time

# sites algorithms
from sites.jd_sports import jd_sports
from sites.terminal_x import terminal_x

# sites urls
jd_sports_url = "https://www.jdsports.co.il/collections/men-shoes-sneakers?page="
terminal_x_url = "https://www.terminalx.com/men/shoes/sneakers-shoes?p="


def main():

    while True:
        jd_sports_process = Process(target=jd_sports.new_product_urls, args=(jd_sports_url, keywords))
        jd_sports_process.start()

        terminal_x_process = Process(target=terminal_x.new_product_urls, args=(terminal_x_url, keywords))
        terminal_x_process.start()

        time.sleep(30)


if __name__ == "__main__":
    main()
