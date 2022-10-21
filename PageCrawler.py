import langdetect as ld
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

class PageCrawler:

    def __init__(self, company):
        self.url = company["url"]

    def search_for_job(self):
        pass

    def map_website(self):
        pass