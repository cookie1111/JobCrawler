import requests
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import seleniumwire.webdriver as webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep


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
        #options.add_argument("--headless")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options,
                                  seleniumwire_options=wire_opt)
        url = f'https://growjo.com/api/companies?order=desc&orderBy=employee_growth&offset=0&rowsPerPage=50&filter={{"industry":"AI","country":"Germany"}}'
        driver.get(url)
        #alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        sleep(3)
        alert = driver.switch_to.alert
        alert.send_input(self.usr)
        alert.send_input(Keys.TAB)
        alert.send_input(self.pwd)
        sleep(60)
        alert.accept()
        ret_id = None
        for request in driver.requests:
            if "auth" in request.headers:
                auth = request.headers["auth"]
                authorization = request.headers["authorization"]
                break

        #driver.close()
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

    def get_companies(self):
        data = requests.get(
            'https://growjo.com/api/companies?order=desc&orderBy=employee_growth&offset=0&rowsPerPage=50&filter={"industry":"AI","country":"Germany"}',
            headers={
                "auth" : self.auth,
                "authorization" : self.authorization
            })


        return data


