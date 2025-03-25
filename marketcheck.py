from bs4 import BeautifulSoup
import requests
import json

api_key = "2fF3nUvfScNJ2V99N3KYDQmFzxhCApSc"
# url = f"https://mc-api.marketcheck.com/v2/search/car/active?api_key={api_key}&year=2024%2C2023%2C2022&make=ford&model=F-150&include_relevant_links=true"
# ex: high value features - https://mc-api.marketcheck.com/v2/search/car/active?api_key={{api_key}}&year=2024&make=ford&include_relevant_links=true&high_value_features=adaptive cruise control&facets=high_value_features
# ex: make/model/trim - https://mc-api.marketcheck.com/v2/search/car/active?api_key={{api_key}}&year=2024&make=ford&model=f-150&trim=XLT&include_relevant_links=true
# ex: condition (new/used/certified) - https://mc-api.marketcheck.com/v2/search/car/active?api_key={{api_key}}&car_type=used&exclude_certified=true&include_relevant_links=true
# ex: https://mc-api.marketcheck.com/v2/search/car/active?api_key={{api_key}}&car_type=used&make=ford&city=Los Angeles&state=ca&zip=91601&msa_code=4480&include_relevant_links=true
# ex: carfax - https://mc-api.marketcheck.com/v2/search/car/active?api_key={{api_key}}&car_type=used&year=2024&make=ford&model=f-150&carfax_1_owner=true&carfax_clean_title=false&include_relevant_links=true
# ex: color - https://mc-api.marketcheck.com/v2/search/car/active?api_key={{api_key}}&car_type=used&year=2024&make=ford&model=f-150&exterior_color=White&include_relevant_links=true
# ex: interior color - https://mc-api.marketcheck.com/v2/search/car/active?api_key={{api_key}}&car_type=used&year=2024&make=ford&model=f-150&interior_color=black&include_relevant_links=true
# ex: distance - https://mc-api.marketcheck.com/v2/search/car/active?api_key={{api_key}}&car_type=used&latitude=34.0222&longitude=-118.2795&radius=200&sort_by=dist&sort_order=desc&include_relevant_links=true
# ex: miles filter - https://mc-api.marketcheck.com/v2/search/car/active?api_key={{api_key}}&car_type=used&year=2024&make=ford&latitude=34.05&longitude=-118.24&radius=100&start=0&rows=50&seller_type=dealer&miles_range=3000-5000
# ex: sort by price - https://mc-api.marketcheck.com/v2/search/car/active?api_key={{api_key}}&year=2024&make=ford&car_type=used&start=0&rows=10&latitude=34.0222&longitude=-118.2795&radius=10&sort_by=price&sort_order=asc
# ex: second page per 10 - https://mc-api.marketcheck.com/v2/search/car/active?api_key={{api_key}}&year=2024&make=ford&latitude=34.0222&longitude=-118.2795&radius=10&car_type=used&start=10&rows=10&sort_by=price
# ex: first page per 25 - https://mc-api.marketcheck.com/v2/search/car/active?api_key={{api_key}}&year=2024&make=ford&latitude=34.0222&longitude=-118.2795&radius=10&car_type=used&start=0&rows=25
# ex: by title type - https://mc-api.marketcheck.com/v2/search/car/auction/active?api_key={{api_key}}&title_type=salvage
# ex: avg car price - https://mc-api.marketcheck.com/v2/search/car/uk/active?api_key={{api_key}}&make=ford&car_type=used&start=1&rows=0&stats=price,miles&latitude=54.87&longitude=-6.228&radius=100


def check(make, model, year):
    url = f"https://mc-api.marketcheck.com/v2/search/car/active?api_key={api_key}&year={year}make={make}&model={model}&include_relevant_links=true"

    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)

    listings = json.loads(response.text)["listings"]
    return listings