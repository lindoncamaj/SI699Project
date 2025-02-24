import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
from statistics import median

class Cars:
    def __init__(self, make, model, year, trim=""):
        HEADERS = ({'User-Agent':
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

        self.make = make
        self.model = model
        self.year = year

        self.url = requests.get(f"https://www.kbb.com/{self.make}/{self.model}/{self.year}/specs/", headers=HEADERS)
        self.soup = BeautifulSoup(self.url.content, "html.parser", from_encoding='utf-8')

    def get_prices(self):
        try:
            fmp = self.soup.find("tbody", {"class": "css-1dfwth1 e1d7xkd05"}).find("tr").get_text()
            prices = fmp.split("Price")[1].split("$")[1:]
            prices = [int(price.replace(",", "")) for price in prices]

            min_price = prices[0]
            med_price = int(median(prices))


            # print(f"{year} {make} {model} Minimum Price: ${min_price}")
            # print(f"{year} {make} {model} Median Price: ${med_price}")
            return {"make": self.make, "model": self.model, "year": self.year, "min_price": min_price, "median_price": med_price}
        except Exception as e:
            print(e)
            print(self.make)
            print(self.model)
            print(self.year)
            return {"make": self.make, "model": self.model, "year": self.year, "min_price": 0, "median_price": 0}


# car_test = Cars("honda", "civic", 2021)
# car_test = Cars("honda", "civic", 2023)
# car_test = Cars("acura", "tlx", 2021)
# car_test = Cars("audi", "q5", 2021)
# car_test = Cars("chevrolet", "corvette", 2021)
# car_test = Cars("toyota", "camry", 2021)