import requests
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import seleniumwire.webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
import json


"""https://growjo.com/api/companies?order=desc&orderBy=employee_growth&offset=0&rowsPerPage=50&filter={"industry":"AI","country":"Germany",}"""

class GrowJoAPI:

    def __init__(self, usr, pwd, log = False, ):
        self.country = "Germany"
        self.field = "AI"
        self.subfield = ""
        self.city = ""
        self.log = log
        self.usr = usr
        self.pwd = pwd
        self.auth, self.authorization = self._get_auth_and_authorization()


    def _get_auth_and_authorization(self):
        options = webdriver.ChromeOptions()

        wire_opt = {}
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36")
        options.add_argument("--headless")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options,
                                  seleniumwire_options=wire_opt)
        url = f'https://growjo.com/login'
        driver.get(url)
        usr = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        usr.send_keys(self.usr)
        pwd = driver.find_element(By.ID, 'password')
        pwd.send_keys(self.pwd)
        pwd.send_keys(Keys.ENTER)

        auth = authorization = None
        sleep(1.1)
        url = f'https://growjo.com/search'
        driver.get(url)
        for request in driver.requests:
            if "auth" in request.headers:
                auth = request.headers["auth"]
                authorization = request.headers["authorization"]

        return auth, authorization

    def set_country(self,country):
        self.country = country
        if self.log : print(self.country, end=", "),
        pass

    def set_field(self, field):
        self.field = field
        if self.log: print(self.field, end=", "),
        pass

    def set_subfield(self, subfield):
        self.subfield = subfield
        if self.log: print(self.subfield, end=", "),
        pass

    def set_city(self, city):
        self.city = city
        if self.log: print(self.city, end=""),
        pass

    def get_filter(self):
        #'{"industry": "AI", "country": "Germany", "subIndustry","3D", "city":"London"}'
        city = ""
        field = ""
        subfield = ""
        country = ""
        if self.city:
            city = f'"city":"{self.city}"'
        if self.country:
            country = f'"country":"{self.country}"'
        if self.field:
            field = f'"industry":"{self.field}"'
        if self.subfield:
            subfield = f'"subIndustry":"{self.subfield}"'
        if city or field or country or subfield:
            filter = f"{(city+',') if city else ''}{(country+',') if country else ''}{(field+',') if field else ''}{(subfield+',') if subfield else ''}"
            if filter[-1] == ',':
                filter = filter[:-1]
            return f"filter={{{filter}}}"
        else:
            return None

    def get_companies(self):
        filter = self.get_filter()
        print(filter)
        response = requests.get(
            #'https://growjo.com/api/companies?order=desc&orderBy=employee_growth&offset=0&rowsPerPage=50&filter={"industry":"AI","country":"Germany"}',
            f'https://growjo.com/api/companies?order=desc&orderBy=employee_growth&offset=0&rowsPerPage=50&{filter if filter else ""}',
            headers={
                "auth" : self.auth,
                "authorization" : self.authorization
            })

        return json.loads(response.text)['data']


