from nike_scrape_functions import *



def main():
    pages_list = []
    products_urls = []
    products_names = []
    products_prices = []
    products_images = []
    products_sizes = []

    scrape_first_products(products_urls, products_names, products_prices, products_images)
    create_scroll_pages_list(api_url, pages_list)
    scrape_api_products_details(pages_list, products_urls, products_names, products_prices, products_images)

    scrape_sizes(products_urls, products_sizes)

    # test prints
    print(products_sizes)
    print(len(products_sizes))
    print(len(products_urls))
    print(len(products_images))
    print(len(products_names))
    print(len(products_prices))


if __name__ == "__main__":
    main()


