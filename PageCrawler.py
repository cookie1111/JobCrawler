import langdetect as ld
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

class PageCrawler:

    def __init__(self, company):
        self.url = company["url"]
        self.urls_internal = set()


    def search_for_job(self):

        pass

    def map_website(self):
        pass

    def get_page_urls(self, url, external_urls):
        urls = set()
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
                    external_urls.add(href)
                continue

            self.urls_internal.add(href)
            urls.add(href)
        return urls, external_urls

    def _check_is_valid_url(self, url):
        parse = urlparse(url)
        return bool(parse.netloc) and bool(parse.scheme)
