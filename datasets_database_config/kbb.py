import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import pandas as pd
from statistics import median

class Cars:
    def __init__(self, make, model="", year="", trim="", extra=False):
        self.HEADERS = ({'User-Agent':
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

        self.make = make
        self.model = model
        self.year = year
        self.extra = extra

        if not self.extra:
            self.url = requests.get(f"https://www.kbb.com/{self.make}/{self.model}/{self.year}/specs/", headers=self.HEADERS)
            self.soup = BeautifulSoup(self.url.content, "html.parser", from_encoding='utf-8')

            self.url2 = requests.get(f"https://www.kbb.com/{self.make}/{self.model}/{self.year}/", headers=self.HEADERS)
            self.soup2 = BeautifulSoup(self.url2.content, "html.parser", from_encoding='utf-8')
        else:
            self.url = requests.get(f"https://www.kbb.com/car-finder/page-1/?manufacturers={self.make}&years={self.year}", headers=self.HEADERS)
            self.soup = BeautifulSoup(self.url.content, "html.parser", from_encoding='utf-8')

            self.url2 = requests.get(f"https://www.kbb.com/{self.make}/{self.model}/{self.year}/specs/", headers=self.HEADERS)
            self.soup2 = BeautifulSoup(self.url2.content, "html.parser", from_encoding='utf-8')

            self.url3 = requests.get(f"https://www.kbb.com/{self.make}/{self.model}/{self.year}/", headers=self.HEADERS)
            self.soup3 = BeautifulSoup(self.url3.content, "html.parser", from_encoding='utf-8')

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
        if self.extra:
            car = self.get_extra_details()
            # print(car)
        else:
            car = {"make": self.make, "model": self.model, "year": self.year}
            image = self.get_image()
            scores = self.get_scores()
            price = self.get_price()
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
            if self.extra:
                return {"image": self.soup3.find("img", {"class": "carousel-image css-ionjye"})["src"]}
            else:
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
            if self.extra:
                scores = self.soup3.find("div", {"class": "css-etwvzw e1qqueke1"}).get_text()
            else:
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

    def get_extra_details(self):
        """
        Function to get trim, drivetrain, enginetype, and combined MPG (gas and electric)) info for a specific make/model/year
        """
        print(self.make)
        print(self.model)
        print(self.year)
        trim_details = {}
        num_trims = int(self.soup2.find("div", {"class": "css-g5d4vu e87bpoh0"}).get_text().split("of ")[1])

        trim_details["make"] = [self.make for _ in range(num_trims)]
        trim_details["model"] = [self.model for _ in range(num_trims)]
        trim_details["year"] = [self.year for _ in range(num_trims)]


        trim_details["trim"] = []
        trims = self.soup2.find_all("div", {"class": "css-1044rcd eds0yfe0"})
        for trim in trims:
            t = trim.get_text().split(f"{num_trims}")[-1]
            trim_details["trim"].append(t)



        table_details = self.soup2.find("table", {"id": "comparetrim-maintable"})
        for row in table_details.tbody.find_all('tr'):
            columns = row.find_all('td')
            trim_details[columns[1].text] = []
            count = 1
            while count <= num_trims:
                trim_details[columns[1].text].append(columns[count+1].text)
                count+=1

        if "5 Year Cost to Own5-Year Cost to Own includes out of pocket expenses like fuel and insurance, plus the car’s loss in value over time (depreciation)." in trim_details.keys():
            trim_details.pop("5 Year Cost to Own5-Year Cost to Own includes out of pocket expenses like fuel and insurance, plus the car’s loss in value over time (depreciation).")

        fuel_type = []
        for ft in trim_details["Fuel Type"]:
            if "LeafIcon" in ft:
                ft = ft.split("Leaf")[0]
                fuel_type.append(ft)
            else:
                fuel_type.append(ft)
        trim_details["Fuel Type"] = fuel_type

        # print(trim_details)
        if "MPGe" in trim_details.keys():
            fuel_economy = trim_details["MPGe"]
            trim_details.pop("MPGe")

            city_fuel_economy = []
            hwy_fuel_economy = []
            comb_fuel_economy = []

            for row in fuel_economy:
                try:
                    nr = row.split("/")

                    city_fuel_economy.append(int(nr[0].split("y ")[1]))
                    hwy_fuel_economy.append(int(nr[1].split("y ")[1]))
                    comb_fuel_economy.append(int(nr[2].split("b ")[1].split()[0]))
                except:
                    city_fuel_economy.append(0)
                    hwy_fuel_economy.append(0)
                    comb_fuel_economy.append(0)

            trim_details["city_fuel_economy"] = city_fuel_economy
            trim_details["hwy_fuel_economy"] = hwy_fuel_economy
            trim_details["comb_fuel_economy"] = comb_fuel_economy
        else:
            if "Fuel Economy" in trim_details.keys():
                fuel_economy = trim_details["Fuel Economy"]
                trim_details.pop("Fuel Economy")
            else:
                fuel_economy = ["" for _ in range(num_trims)]

            city_fuel_economy = []
            hwy_fuel_economy = []
            comb_fuel_economy = []

            for row in fuel_economy:
                try:
                    nr = row.split("/")

                    city_fuel_economy.append(int(nr[0].split("y ")[1]))
                    hwy_fuel_economy.append(int(nr[1].split("y ")[1]))
                    comb_fuel_economy.append(int(nr[2].split("b ")[1].split()[0]))
                except:
                    city_fuel_economy.append(0)
                    hwy_fuel_economy.append(0)
                    comb_fuel_economy.append(0)

            trim_details["city_fuel_economy"] = city_fuel_economy
            trim_details["hwy_fuel_economy"] = hwy_fuel_economy
            trim_details["comb_fuel_economy"] = comb_fuel_economy

        drivetrain_table_details = self.soup2.find("table", {"id": "super-table-accordion_mechanical"})
        for row in drivetrain_table_details.tbody.find_all('tr'):
            columns = row.find_all('td')
            trim_details[columns[1].text] = []
            count = 1
            while count <= num_trims:
                trim_details[columns[1].text].append(columns[count+1].text)
                count+=1

        if "Fair Market Price" in trim_details.keys():
            trim_details['min_price'] = trim_details.pop('Fair Market Price')
        else:
            trim_details['min_price'] = trim_details.pop('MSRP')

        prices = []
        for i in range(num_trims):
            prices.append(int(trim_details["min_price"][i].replace(",", "").split("$")[1]))
        trim_details["min_price"] = prices
        med_price = int(median(prices))
        trim_details["med_price"] = [med_price for _ in range(num_trims)]

        images = self.get_image()
        scores = self.get_scores()
        trim_details["image"] = [images["image"] for _ in range(num_trims)]
        trim_details["expert_score"] = [scores["expert_score"] for _ in range(num_trims)]
        trim_details["consumer_score"] = [scores["consumer_score"] for _ in range(num_trims)]

        trim_details = {key.lower().replace(' ', '_'): value for key, value in trim_details.items()}
        trim_details = {key: trim_details[key] for key in ["make", "model", "year", "trim", "fuel_type", "drivetrain", "city_fuel_economy", "hwy_fuel_economy", "comb_fuel_economy", "transmission_type", "min_price", "med_price", "image", "expert_score", "consumer_score"] if key in trim_details}

        cars_list = []
        for i in range(num_trims):
            car_details = {key: values[i] for key, values in trim_details.items()}
            cars_list.append(car_details)

        return cars_list



    def get_new_cars(self):
        """
        Function to get make/models/years for cars of a certain make within a certain range of years
        """
        cars = []
        last_page = False
        page = 1
        while not last_page:
            print(f"page number {page}")
            test = self.soup.find_all("a", {"class": "css-z66djy ewtqiv30"})
            # for t in test:
            #     print(t)
            #     cars.append(t.get("href").split("/")[1:4])
            test = self.soup.find_all("h2", {"class": "css-iqcfy5 e148eed12"})
            for t in test:
                car = t.get_text()
                year = car.split()[0]
                model = car.lower().split(f"{self.make} ")[-1].replace(" ", "-")
                cars.append([self.make, model, year])

            page +=1
            self.url = requests.get(f"https://www.kbb.com/car-finder/page-{page}/?manufacturers={self.make}&years={self.year}", self.HEADERS)
            self.soup = BeautifulSoup(self.url.content, "html.parser", from_encoding='utf-8')
            if "We were unable to find any matches to your search." in self.soup.get_text():
                last_page = True
        print(cars)
        print("hit last page")
        return cars

# car_test = Cars("honda", "civic-hybrid", 2025, extra=True)
# car_test.get_car()
# car_test = Cars("honda", "civic", 2019)
# car_test.get_car()
# car_test = Cars("acura", "tlx", 2021)
# car_test.get_car()
# car_test = Cars("audi", "q5", 2021, extra=True)
# car_test.get_car()
# car_test = Cars("chevrolet", "corvette", 2021)
# car_test.get_car()
# car_test = Cars("ferrari", "roma", 2023)
# car_test.get_car()
# car_test = Cars("tesla", "model-3", 2022, extra=True)
# car_test.get_car()

# car_test = Cars("tesla", year="2021-2026")
# car_test.get_new_cars()
# car_test = Cars("bmw", "x6", 2025, extra=True)
# car_test.get_car()

# car_test = Cars("bmw", year="2021-2026")
# car_test.get_new_cars()

# car_test = Cars("honda", year="2021-2026")
# car_test.get_new_cars()

# 'chrysler', 'hyundai', 'jeep', 'volkswagen'
makes = [
    'chrysler', 'hyundai', 'jeep', 'volkswagen'
]

models = []
for make in makes:
    car_test = Cars(make, year="2010-2024", extra=True)
    new_models = car_test.get_new_cars()
    models.extend(new_models)


all_car_data = []
bad_models = []
for m in models:
    try:
        car = Cars(m[0], m[1], m[2], extra=True)
        extra_details = car.get_extra_details()
        all_car_data.extend(extra_details)
    except:
        bad_models.append(m)


car_df = pd.DataFrame(all_car_data)
car_df.to_csv("all_makes_models6.csv", index=False)


print(bad_models)