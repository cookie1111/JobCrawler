import requests
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import seleniumwire.webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
from typing import Tuple, List, Dict
import json


"""https://growjo.com/api/companies?order=desc&orderBy=employee_growth&offset=0&rowsPerPage=50&filter={"industry":"AI","country":"Germany",}"""

class GrowJoAPI:

    def __init__(self, usr: str, pwd: str, log: bool = False, ) -> None:
        """
        creates the GrowJoApi class and gets the auth and authorization header fields

        :param usr: username store it in a seperate file and load it in
        :param pwd: password store it in a seperate file and load it in
        :param log: show log if True
        """
        self.country = "Germany"
        self.field = "AI"
        self.subfield = ""
        self.city = ""
        self.log = log
        self.usr = usr
        self.pwd = pwd
        self.auth, self.authorization = self._get_auth_and_authorization

    @property
    def _get_auth_and_authorization(self) -> Tuple[str, str]:
        """
        grabs auth and authorization by logging you in and grabbing the header fields using selenium_wire

        :return: auth and authorization header fields
        """
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
        if self.log:
            print(auth, authorization)
        return auth, authorization

    def set_country(self, country: str) -> None:
        """
        sets the country field of the search

        :param country: name of country
        """
        self.country = country
        if self.log : print(self.country, end=", "),
        pass

    def set_field(self, field: str) -> None:
        """
        sets the industry field of the search

        :param field: name of industry
        """
        self.field = field
        if self.log: print(self.field, end=", "),
        pass

    def set_subfield(self, subfield: str) -> None:
        """
        set the sub industry field of the search

        :param subfield: name of subindustry
        """
        self.subfield = subfield
        if self.log: print(self.subfield, end=", "),
        pass

    def set_city(self, city: str) -> object:
        """
        set the city field of the search

        :param city: name of city
        """
        self.city = city
        if self.log: print(self.city, end=""),
        pass

    def get_filter(self) -> str:
        """
        constructs the filter string

        :return: constructed filter string
        """
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
            return "filter={}"

    def get_companies(self, page: int = 0, rows: int = 50) -> Tuple[List[Dict], int]:
        """
        grab company list(paged) call repeatedly with different page value to scroll through

        :param page: page of the data
        :param rows: amount of data per apge
        :return: (list of companies, amount of found companies)
        """
        filter = self.get_filter()
        print(filter)
        response = requests.get(
            #'https://growjo.com/api/companies?order=desc&orderBy=employee_growth&offset=0&rowsPerPage=50&filter={"industry":"AI","country":"Germany"}',
            f'https://growjo.com/api/companies?order=desc&orderBy=employee_growth&offset={page*rows}&rowsPerPage={rows}&{filter if filter else ""}',
            headers={
                "auth" : self.auth,
                "authorization" : self.authorization
            })

        return json.loads(response.text)['data'],json.loads(response.text)['totalCount']


