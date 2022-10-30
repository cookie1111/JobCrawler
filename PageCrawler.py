import langdetect as ld
import requests
import queue
from time import sleep
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator as Translator
from urllib.parse import urlparse
from pathlib import Path

class PageCrawler:

    def __init__(self, company, search_for = ["career", "we-are-recruiting","we-are-hiring", "job", "positions", "welcomekit", "joinus", "join-us", "recruit","work-with-us","work-for-us"]):
        self.url = "https://" + company["url"]
        if not self._try_url():
            self.dead_link = True
        else:
            self.dead_link = False
        if not self.dead_link:
            self.compare_list = search_for
            self.compare_list = self.add_translations(self.get_language())
            self.urls_internal = set([self.url])
            self.urls_queue = queue.Queue()
            self.urls_queue.put(self.url)
            self.potential_job_pages = set()

    def _try_url(self):
        try:
            response = requests.get(self.url,timeout=3)
            response.raise_for_status()
            return True
        except requests.exceptions.HTTPError as e:
            print(self.url, ": ", e)
            return False
        except requests.exceptions.Timeout as e:
            print(self.url,": ", e)
            return False
        except requests.exceptions.TooManyRedirects as e:
            print(self.url, ": ", e)
            return False
        except requests.exceptions.SSLError as e:
            print(self.url, ": ", e)
            return False
        except requests.exceptions.ConnectionError as e:
            print(self.url, ": ", e)
            return False


    def search_for_job_page(self, url):
        parsed = urlparse(url)
        for w in self.compare_list:
            if w in parsed.path:
                return True
        return False

    def get_about_us(self, urls):
        pass

    def get_language(self):
        soup = BeautifulSoup(requests.get(self.url).content, 'html.parser')
        text_page = soup.get_text()
        return ld.detect(text_page)

    def add_translations(self, lang):
        t = Translator(source='en', target=lang)
        return self.compare_list + t.translate_batch(self.compare_list)

    def map_first_page_only(self):
        # init the crawl
        external_urls = set()
        if self.search_for_job_page(self.url):
            self.potential_job_pages.add(self.url)
        urls, external_urls_new = self.get_page_urls(self.url, external_urls)
        # check external links for jobs
        self._check_external_urls(external_urls_new)
        external_urls = external_urls.union(external_urls_new)
        # check internal links for jobs
        print(urls)
        for url in list(urls):
            if self.search_for_job_page(url):
                self.potential_job_pages.add(url)

        potential_job_internal = set()
        potential_job_external = set()
        if len(self.potential_job_pages):
            for job_page in list(self.potential_job_pages):
                job_internal, job_external = self.get_page_urls(job_page, external_urls)
                potential_job_internal.update(job_internal)
                potential_job_external.update(job_external)
        return self.potential_job_pages, potential_job_internal, potential_job_external

    def map_website_n_deep_save_html(self, n=2, max_pages = 100, path = "/urls"):
        cur_lvl = set([self.url])
        overall = set([self.url])
        external = set()
        next_lvl = set()
        for i in range(n):
            print("depth: ",i," amount: ",len(cur_lvl))
            for url in cur_lvl:
                cur, ext, html = self.get_page_urls(url, external, return_html=True)
                if html is None:
                    continue
                url = url.replace('https://','')
                url = url.replace('/','-')
                if not Path(path+'/' + url.replace('.', '_') + '.html').is_file():
                    with open(path+'/' + url.replace('.', '_') + '.html', 'wb+') as f:
                        #figure out a naming convention
                        f.write(html)
                grabbed = cur.difference(overall)
                if len(grabbed) > max_pages:
                    sleep(0.05)
                    continue
                next_lvl = next_lvl.union(cur.difference(overall))
                # for now we don't grab external pages
                # next_lvl.add(ext.difference(external))
                sleep(0.05)
            overall = overall.union(next_lvl)
            cur_lvl = next_lvl
            next_lvl = set()

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
            print(list(self.urls_queue.queue))
            url = self.urls_queue.get()
            if self.search_for_job_page(url):
                return self.potential_job_pages
            try:
                urls, external_urls_new = self.get_page_urls(url, external_urls)
            except requests.exceptions.InvalidSchema:
                print("This url leads nowhere: ", url)
            self._check_external_urls(external_urls_new)
            external_urls = external_urls.union(external_urls_new)
            sleep(0.3)

        if len(self.potential_job_pages) == 0:
            print(self.url, ": no job page found!")

        return self.potential_job_pages

    # possible alternative
    def find_career_button(self):
        pass

    def get_page_urls(self, url, external_urls, return_html = False):
        """

        :rtype: set(internal_urls),set(external_urls) or -||- + html of page
        """
        urls = set()
        external_urls_new = set()
        domain = urlparse(url).netloc
        try:
            re = requests.get(url, timeout=3)
            soup = BeautifulSoup(re.content, "html.parser")
        except requests.exceptions.Timeout as e:
            print(url, ": ", e)
            if return_html:
                return urls, external_urls_new, None
            return urls, external_urls_new
        except requests.exceptions.HTTPError as e:
            print(url, ": ", e)
            if return_html:
                return urls, external_urls_new, None
            return urls, external_urls_new
        except requests.exceptions.TooManyRedirects as e:
            print(url, ": ", e)
            if return_html:
                return urls, external_urls_new, None
            return urls, external_urls_new
        except requests.exceptions.SSLError as e:
            print(url, ": ", e)
            if return_html:
                return urls, external_urls_new, None
            return urls, external_urls_new
        except requests.exceptions.ConnectionError as e:
            print(url, ": ", e)
            if return_html:
                return urls, external_urls_new, None
            return urls, external_urls_new

        for linkie in soup.findAll('a'):
            href = linkie.attrs.get("href")
            #invalid linkie
            if href == "" or href is None:
                continue

            href = urljoin(url, href)

            parse_href = urlparse(href)
            href = parse_href.scheme + "://" + parse_href.netloc + parse_href.path
            try:
                if not self._check_is_valid_url(href) or href in self.urls_internal:
                    continue
            except ValueError as e:
                print(href, ": ", e)
                continue
            if domain not in href:
                if href not in external_urls:
                    external_urls_new.add(href)
                continue

            self.urls_internal.add(href)
            #print(href)
            self.urls_queue.put(href)
            urls.add(href)
        if return_html:
            return urls,external_urls_new, re.content
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
