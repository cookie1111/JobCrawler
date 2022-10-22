import langdetect as ld
import requests
import queue
from time import sleep
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

class PageCrawler:

    def __init__(self, company, search_for = ["career", "we-are-recruiting","we-are-hiring", "job", "positions", "welcomekit", "joinus", "join-us", "recruit"]):
        self.compare_list = search_for
        self.url = company["url"]
        self.urls_internal = set(self.url)
        self.urls_queue = queue.Queue()
        self.urls_queue.put(self.url)
        self.potential_job_pages = set()


    def search_for_job_page(self, url):
        for w in self.compare_list:
            if w in url:
                return True
        return False

    def get_about_us(self, urls):
        pass

    def map_website(self):
        #init the crawl
        external_urls = set()
        if self.search_for_job_page(self.url):
            self.potential_job_pages.add(self.url)
        urls, external_urls_new = self.get_page_urls(self.url, external_urls)
        #check external links for jobs
        self._check_external_urls(external_urls_new)
        external_urls = external_urls.union(external_urls_new)
        while not self.urls_queue.empty():
            url = self.urls_queue.get()
            if self.search_for_job_page(url):
                self.potential_job_pages.add(url)
            try:
                urls, external_urls_new = self.get_page_urls(url, external_urls)
            except requests.exceptions.InvalidSchema:
                print("This url leads nowhere: ", url)
            self._check_external_urls(external_urls_new)
            external_urls = external_urls.union(external_urls_new)
            sleep(0.3)
        if len(self.potential_job_pages):
            print(self.url, ": no job page found!")

        return self.potential_job_pages


    #possible alternative
    def find_career_button(self, ):
        pass

    def get_page_urls(self, url, external_urls):
        urls = set()
        external_urls_new = set()
        domain = urlparse(url).netloc
        soup = BeautifulSoup(requests.get(url).content, "html.parser")

        for linkie in soup.findAll('a'):
            href = linkie.attrs.get("href")
            #invalid linkie
            if href == "" or href is None:
                continue

            href = urljoin(url, href)

            parse_href = urlparse(href)
            href = parse_href.scheme + "://" + parse_href.netloc + parse_href.path
            if not self._check_is_valid_url(href) or href in self.urls_internal:
                continue

            if domain not in href:
                if href not in external_urls:
                    external_urls_new.add(href)
                continue

            self.urls_internal.add(href)
            #print(href)
            self.urls_queue.put(href)
            urls.add(href)
        return urls, external_urls_new

    def _check_external_urls(self, external_urls):
        for url in external_urls:
            pass
        pass

    #navigate welcome to the jungle page
    def _welcome_to_the_jungle(self, url):
        pass


    def _check_is_valid_url(self, url):
        parse = urlparse(url)
        return bool(parse.netloc) and bool(parse.scheme)
