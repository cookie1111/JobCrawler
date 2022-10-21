import GrowJoAPI
from PageCrawler import PageCrawler

page_crawler = PageCrawler({"url" : "https://neuralink.com/"})



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(page_crawler.get_page_urls("https://neuralink.com/",set()))


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
