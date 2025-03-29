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

        self.url2 = requests.get(f"https://www.kbb.com/{self.make}/{self.model}/{self.year}/", headers=HEADERS)
        self.soup2 = BeautifulSoup(self.url2.content, "html.parser", from_encoding='utf-8')

    def get_car(self):
        """
        Function to get necessary image, price, and score information for a specific car make/model/year

        Parameters
        ----------
        none

        Returns
        -------
        dict with all necessary image, price, and score information
        """
        car = {"make": self.make, "model": self.model, "year": self.year}
        image = self.get_image()
        price = self.get_price()
        scores = self.get_scores()

        car = car | image | price | scores
        print(car)
        return car

    def get_image(self):
        """
        Function to get the image link for a car

        Parameters
        ----------
        none

        Returns
        -------
        dict with the image link
        """
        try:
            return {"image": self.soup2.find("img", {"class": "carousel-image css-ionjye"})["src"]}
        except Exception as e:
            print(e)

            return {"image": ""}

    def get_price(self):
        """
        Function to get the minimum and median price of a specific car make/model/year (based on all trims)

        Parameters
        ----------
        none

        Returns
        -------
        dict with the image link
        """
        try:
            fmp = self.soup.find("tbody", {"class": "css-1dfwth1 e1d7xkd05"}).find("tr").get_text()
            prices = fmp.split("Price")[1].split("$")[1:]
            prices = [int(price.replace(",", "")) for price in prices]

            min_price = prices[0]
            med_price = int(median(prices))

            return {"min_price": min_price, "median_price": med_price}
        except Exception as e:
            print(e)

            return {"min_price": 0, "median_price": 0}

    def get_scores(self):
        """
        Function to get expert and consumer scores for a car

        Parameters
        ----------
        none

        Returns
        -------
        dict with the expert and consumer scores
        """
        try:
            scores = self.soup2.find("div", {"class": "css-etwvzw e1qqueke1"}).get_text()

            if scores[0] == "E":
                expert = 0
                try:
                    consumer = float(scores[12:15])
                except:
                    consumer = 0
                s = {"expert_score": expert, "consumer_score": consumer}
                return s
            else:
                expert = float(scores[:3])
                try:
                    consumer = float(scores[9:12])
                except:
                    consumer = 0
                s = {"expert_score": expert, "consumer_score": consumer}
                return s
        except Exception as e:
            print(e)

            return {"expert_score": 0, "consumer_score": 0}


# car_test = Cars("honda", "civic", 2021)
# car_test.get_car()
# car_test = Cars("honda", "civic", 2019)
# car_test.get_car()
# car_test = Cars("acura", "tlx", 2021)
# car_test.get_car()
# car_test = Cars("audi", "q5", 2021)
# car_test.get_car()
# car_test = Cars("chevrolet", "corvette", 2021)
# car_test.get_car()
# car_test = Cars("ferrari", "roma", 2023)
# car_test.get_car()