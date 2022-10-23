from GrowJoAPI import GrowJoAPI
from PageCrawler import PageCrawler
from time import sleep



page_crawler = PageCrawler({"url" : "https://neuralink.com/"})
grow_jo = GrowJoAPI(auth, authorization, log = True)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # crawler tests
    print(page_crawler.get_page_urls("https://neuralink.com/",set()))
    #print(page_crawler.map_website())

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

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
