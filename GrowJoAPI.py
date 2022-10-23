import requests

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
        return 1,1

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


