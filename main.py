import math
import signal
import sys
import time

from requests.adapters import HTTPAdapter
from guppy import hpy; h = hpy()

from GrowJoAPI import GrowJoAPI
from PageCrawler import PageCrawler
from time import sleep
import pandas as pd
from os.path import isfile
from pathlib import Path
import concurrent.futures as ft
import requests
from langdetect.detector_factory import init_factory

TEST = 4
DF_FILE = "sites.pkl"
PAGES_PATH = "pages_ds/"

# implement: https://stackoverflow.com/questions/53493973/how-to-pause-processes-in-case-they-are-consuming-too-much-memory
# https://stackoverflow.com/questions/20776189/concurrent-futures-vs-multiprocessing-in-python-3
# to help with RAM management

def innit_corpus():
    global sess
    sess = requests.Session()
    sess.mount("http://", HTTPAdapter(max_retries=10))
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    init_factory()

def create_crawler_and_run_it(url, path):
    # print("working on url")
    craw = PageCrawler({"url":url})
    Path(path).mkdir(parents=True, exist_ok=True)
    craw.map_website_n_deep_save_html(n=3,path=path,with_external=True)

with open("usr.txt", 'r') as f:
    lines = f.read().splitlines()
    usr = lines[0]
    pwd = lines[1]
    print(usr,pwd)

#page_crawler = PageCrawler({"url" : "simreka.com"})
#grow_jo = GrowJoAPI(usr, pwd, log = True)
if isfile(DF_FILE):
    df = pd.read_pickle(DF_FILE)
else:
    df = pd.DataFrame(columns = ['Company_Name', 'URL', 'Career', 'Internal_Potential_Job', 'External_Potential_Job'])


if __name__ == '__main__':
    grow_jo = GrowJoAPI(usr=usr, pwd=pwd, log=True)
    if TEST == 0:
    # crawler tests
        pass
        #print(page_crawler.map_first_page_only())
        #print(page_crawler.map_website())

    if TEST == 1:

        # GrowJo tests
        # empty
        grow_jo.set_city("")
        grow_jo.set_country("")
        grow_jo.set_field("")
        grow_jo.set_subfield("")
        print(": ",grow_jo.get_companies())

        sleep(0.2)

        # incorrect
        grow_jo.set_city("33")
        grow_jo.set_country("asfasf")
        grow_jo.set_field("awd")
        grow_jo.set_subfield("warfaf")
        print(": ",grow_jo.get_companies())

        sleep(0.2)

        # correct with missing fields
        grow_jo.set_city("")
        grow_jo.set_country("Germany")
        grow_jo.set_field("AI")
        grow_jo.set_subfield("")
        print(": ",grow_jo.get_companies())

        sleep(0.2)

        # correct with missing fields
        grow_jo.set_city("")
        grow_jo.set_country("Germany")
        grow_jo.set_field("AI")
        grow_jo.set_subfield("")
        print(": ",grow_jo.get_companies())

    if TEST == 2:
        #grow_jo.get_companies()
        pass

    if TEST == 3:
        grow_jo.set_field('')

        #print(len(data))
        #sys.exit()
        data,amount = grow_jo.get_companies()
        for i in range(int(math.ceil(amount/50))):
            data, amount = grow_jo.get_companies(page=i)
            start = time.process_time_ns()
            for company in data:
                print(company["company_name"])
                if not df['Company_Name'].str.contains(company['company_name'], regex=False).any():
                    try:
                        pc = PageCrawler(company)
                    except:
                        continue
                    if pc.dead_link:
                        continue
                    career, internal_jobs, external_jobs = pc.map_first_page_only()
                    df = df.append({'Company_Name': company['company_name'], 'URL': company['url'], 'Career': list(career), 'Internal_Potential_Job' : list(internal_jobs), 'External_Potential_Job' : list(external_jobs)}, ignore_index=True)
                    df.to_pickle(DF_FILE)
            delta = time.process_time_ns() -start
            if delta < 1000000000:
                time.sleep((1000000000-delta)/1000000000)

    if TEST == 4:
        executor = ft.ProcessPoolExecutor(5,initializer=innit_corpus)
        start = 920
        cnt = 1000
        with ft.ProcessPoolExecutor(5,initializer=innit_corpus) as executor:
            while start<cnt:
                #print(df.shape)
                futs = [executor.submit(create_crawler_and_run_it, url, PAGES_PATH+url.replace('.', '_')) for url in df.URL.iloc[start:start+5]]
                ft.wait(futs)
                #print(h.heap())
                start = start + 5
                print(start)
        #futs = [executor.submit(create_crawler_and_run_it, url, PAGES_PATH+url.replace('.', '_')) for url in df.URL.iloc[140:1000]]
        #ft.wait(futs)
        for res in futs:
            print(res.result())
        """for url in df.URL.iloc[160:]:
            print(url,":")
            create_crawler_and_run_it(url,PAGES_PATH + url.replace('.','_'))
        """