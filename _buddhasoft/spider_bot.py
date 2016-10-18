# This Python file uses the following encoding: utf-8
from selenium import webdriver
# from ad_class import Ad
import os
import xlsxwriter as xl
# from docx import Document

class Ad:
    def __init__(self, url, title, price, owner_name, added_date, location, product_condition, descripton):
        self.url = url
        self.title = title
        self.price = price
        self.owner_name = owner_name
        self.added_date = added_date
        self.location = location
        self.product_condition = product_condition
        self.description = descripton


class Scrapper:
    WEB_DRIVERS = {
        'Chrome': 'chromedriver',
        'Firefox': 'geckodriver',
        'Opera': 'operadriver'
    }
    def __init__(self, browser_name='Chrome'):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        complete_path = os.path.join(base_dir, self.WEB_DRIVERS[browser_name])
        self.browser = eval("webdriver.%s" % browser_name)(executable_path=complete_path)
        

    def search(self, query):
        self.parsed_elements = []
        self.browser.get("https://olx.ua")
        elem = self.browser.find_element_by_css_selector("input#headerSearch")
        elem.send_keys(query + '\n')
        elements_with_links = self.browser.find_elements_by_css_selector('h3 > a.detailsLink')  # ищет по названию
        links = [x.get_attribute('href') for x in elements_with_links]
        for link in links:
            self.browser.get(link)
            title = self.browser.find_element_by_css_selector('h1.brkword').text
            price = self.browser.find_elements_by_css_selector('div.pricelabel')[0].text
            owner_name = self.browser.find_elements_by_css_selector('div.userdetails > span.xx-large')[0].text
            added_date = self.browser.find_elements_by_css_selector('span.pdingleft10.brlefte5')[0].text.split(',')[1]
            address = self.browser.find_elements_by_css_selector('strong.c2b')[0].text
            product_condition = self.browser.find_elements_by_css_selector('strong > a')[3].text
            description = self.browser.find_element_by_css_selector('p.pding10').text
            self.parsed_elements.append(Ad(link,
                                      title,
                                      price,
                                      owner_name,
                                      added_date,
                                      address,
                                      product_condition,
                                      description))

    def write_to_xlsx(self):
        workbook = xl.Workbook('results.xlsx')
        worksheet = workbook.add_worksheet()
        col, row = 0, 1
        i = 0
        try:
            for key in self.parsed_elements[0].__dict__.keys():
                worksheet.write(0, i, key)
                i += 1
        except:
            worksheet.write(0, i, 'No value found')
            i += 1

        try:
            for key in self.parsed_elements[col].__dict__.keys():
                for value in self.parsed_elements[row].__dict__.values():
                    worksheet.write(row, col, value)
                    col += 1
                row += 1
                col = 0
        except:
            pass

        workbook.close()

pauk = Scrapper()
pauk.search('iPone7')
pauk.write_to_xlsx()
