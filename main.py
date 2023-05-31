from multiprocessing import Process
from keys import keywords
import time

# sites algorithms
from sites.jd_sports import jd_sports
from sites.terminal_x import terminal_x
from sites.factory_54 import factory_54
from sites.sneakerboxtlv import sneakerboxtlv
from sites.notforsale import notforsale

# sites urls
jd_sports_urls = ["https://www.jdsports.co.il/collections/men-shoes-sneakers?page=", "https://www.jdsports.co.il/collections/women-shoes-sneakers?page="]
terminal_x_url = "https://www.terminalx.com/men/shoes/sneakers-shoes?p="
factory_54_url = ["https://www.factory54.co.il/men-shoes-sneakers?start="]
sneakerboxtlv_url = "https://sneakerboxtlv.com/wp-admin/admin-ajax.php"
notforsale_url = "https://notforsaletlv.com/collections/sneakers?page="


def main():

    while True:
        jd_sports_process = Process(target=jd_sports.new_product_urls, args=(jd_sports_urls, keywords))
        jd_sports_process.start()

        terminal_x_process = Process(target=terminal_x.new_product_urls, args=(terminal_x_url, keywords))
        terminal_x_process.start()

        factory_54_process = Process(target=factory_54.new_product_urls, args=(factory_54_url, keywords))
        factory_54_process.start()

        sneakerboxtlv_process = Process(target=sneakerboxtlv.new_product_urls, args=(sneakerboxtlv_url, keywords))
        sneakerboxtlv_process.start()

        notforsale_process = Process(target=notforsale.new_product_urls, args=(notforsale_url, keywords))
        notforsale_process.start()

        time.sleep(30)


if __name__ == "__main__":
    main()
