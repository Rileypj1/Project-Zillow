##Webscraping apartments in different Philly neighborhoods with Zillow's api
from bs4 import BeautifulSoup
import requests
from requests.auth import HTTPBasicAuth

fishtownURL = "https://www.zillow.com/fishtown-philadelphia-pa/rentals"
header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36'}

fishtownPage = requests.get(fishtownURL, headers= header)

soup = BeautifulSoup(fishtownPage.content, "html.parser")

fishtownApartments = soup.find_all("div", class_="list-card-info")

for apartment in fishtownApartments:
    address_element = apartment.find("address", class_="list-card-addr")
    price_element = apartment.find("div", class_="list-card-price")
    apt_details_element = apartment.find("ul", class_="list-card-details")
    print(address_element.text.strip())
    print(price_element.text.strip())
    print(apt_details_element.text.strip())
    