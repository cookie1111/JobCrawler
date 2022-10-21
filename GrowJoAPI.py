

"""https://growjo.com/api/companies?order=desc&orderBy=employee_growth&offset=0&rowsPerPage=50&filter={"industry":"AI","country":"Germany"}"""

class GrowJoAPI:

    def __init__(self):
        self.country = ""
        self.field = ""
        self.subfield = ""
        self.city = ""


    def set_country(self,country):
        self.country = country
        pass

    def set_field(self, field):
        self.field = field
        pass

    def set_subfield(self, subfield):
        self.subfield = subfield
        pass

    def set_city(self, city):
        self.city = city
        pass