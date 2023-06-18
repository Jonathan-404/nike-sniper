from multiprocessing import Process
from keys import keywords
import time

# sites algorithms
from src.jd_sports import jd_sports
from src.terminal_x import terminal_x
from src.sneakerboxtlv import sneakerboxtlv
from src.notforsale import notforsale
from src.nike import nike
# from src.factory_54 import factory_54





# sites urls
jd_sports_urls = ["https://www.jdsports.co.il/collections/men-shoes-sneakers?page=", "https://www.jdsports.co.il/collections/women-shoes-sneakers?page="]
terminal_x_url = "https://www.terminalx.com/men/shoes/sneakers-shoes?p="
sneakerboxtlv_url = "https://sneakerboxtlv.com/wp-admin/admin-ajax.php"
notforsale_url = "https://notforsaletlv.com/collections/sneakers?page="
nike_url = "https://www.nike.com/il/w/mens-shoes-nik1zy7ok"
# factory_54_url = ["https://www.factory54.co.il/men-shoes-sneakers?start="]


def main():
    print("Starting...")
    while True:

        processes = []  # List to store the processes

        # Create and start the processes
        jd_sports_process = Process(target=jd_sports.get, args=(jd_sports_urls, keywords))
        processes.append(jd_sports_process)

        terminal_x_process = Process(target=terminal_x.get, args=(terminal_x_url, keywords))
        processes.append(terminal_x_process)

        sneakerboxtlv_process = Process(target=sneakerboxtlv.get, args=(sneakerboxtlv_url, keywords))
        processes.append(sneakerboxtlv_process)

        notforsale_process = Process(target=notforsale.get, args=(notforsale_url, keywords))
        processes.append(notforsale_process)

        nike_first_process = Process(target=nike.get_first, args=(nike_url, keywords))
        processes.append(nike_first_process)

        nike_api_process = Process(target=nike.get_api, args=(nike_url, keywords))
        processes.append(nike_api_process)

        # Start all processes
        for process in processes:
            process.start()

        # Wait for all processes to finish
        for process in processes:
            process.join()


if __name__ == "__main__":
    main()
