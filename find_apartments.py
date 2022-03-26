##Webscraping apartments in different Philly neighborhoods with Zillow's api
from bs4 import BeautifulSoup
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd


class ZillowScraper:
    def __init__(self):
        self.header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36'}

    def getUrl(self, neighborhood):
        URL = "https://www.zillow.com/{}-philadelphia-pa/rentals".format(neighborhood)
        neighborhood_page = requests.get(URL, headers= self.header)
        soup = BeautifulSoup(neighborhood_page.content, "html.parser")
        return soup

    def extractData(self, soup, neighborhood):

        neighborhood_apartments = soup.find_all("div", class_="list-card-info")
        neighborhood_list = []
        #some elements on the webpage are NoneType which will throw errors here. we need a try and except to skip those so the for loop functions as expected.
        try:
            for apartment in neighborhood_apartments:
                apt_list = []
                address = apartment.find("address", class_="list-card-addr").text.strip()
                price = apartment.find("div", class_="list-card-price").text.strip()
                apt_details = apartment.find("ul", class_="list-card-details").text.strip()
                neighborhood_string = neighborhood
                apt_list.extend([address,price,apt_details,neighborhood_string])
                apt_list = [i for i in apt_list if i]
                neighborhood_list.append(apt_list)
                # do something with item
        except Exception as e:
            # handle the exception accordingly
            pass
        #remove empty strings
        print("extract function list", type(neighborhood_list))

        return neighborhood_list
    
    def cleanUpNeighborhood(self, neighborhoods):
        columns = ['Address', 'Price', 'Apt_Details', 'Neighborhood']
        print(type(neighborhoods), "\n"*2)
        cleaned_df = pd.DataFrame(neighborhoods, columns = columns)
        print(cleaned_df)


if __name__ == "__main__":
    zillow = ZillowScraper()
    fishtown_page = zillow.getUrl("fishtown")
    fishtown_list = zillow.extractData(fishtown_page,"Fishtown")
    zillow.cleanUpNeighborhood(fishtown_list)

