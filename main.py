from GrowJoAPI import GrowJoAPI
from PageCrawler import PageCrawler
from time import sleep

TEST = 1

with open("usr.txt",'r') as f:
    lines = f.read().splitlines()
    usr = lines[0]
    pwd = lines[1]

page_crawler = PageCrawler({"url" : "https://neuralink.com/"})
grow_jo = GrowJoAPI(usr, pwd, log = True)




if __name__ == '__main__':
    if TEST == 0:
    # crawler tests
        print(page_crawler.get_page_urls("https://neuralink.com/",set()))
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


