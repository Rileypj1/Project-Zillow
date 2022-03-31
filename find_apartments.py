##Webscraping apartments in different Philly neighborhoods with Zillow's api
from bs4 import BeautifulSoup
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import re
import json
from datetime import date


class ZillowScraper:
    def __init__(self):
        self.header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36'}

    def getUrl(self, neighborhood):
        URL = "https://www.zillow.com/{}-philadelphia-pa/rentals".format(neighborhood)
        neighborhood_page = requests.get(URL, headers= self.header)
        soup = BeautifulSoup(neighborhood_page.text, "lxml")
        return soup

    def convertToJSON(self, soup):
        listings = soup.find_all("script")
        #some elements on the webpage are NoneType which will throw errors here. we need a try and except to skip those so the for loop functions as expected.
        #remove html tags
        li_strings = []
        for li in listings:
            li1 = li.get_text().strip()
            li_strings.append(li1)
        r = re.compile("hdpData")
        newlist = list(filter(r.findall, li_strings))
        newlist = [el.replace('-->','') for el in newlist]
        newlist = [el.replace('<!--','') for el in newlist]

        json_list_original = []
        for el in range(len(newlist)):
            json_dict = json.loads(newlist[el])
            json_list_original.append(json_dict)
        #with list of strings, find nested json objects that contain relevant data
        json_list_cleaned = json_list_original[0]['cat1']['searchResults']['listResults']
        return json_list_cleaned
    
    def extractData(self, soup, neighborhood):

        json_data = self.convertToJSON(soup)


        neighborhood_list = []
        for li in range(len(json_data)):
            try:        
                li_dict = json_data[li]['hdpData']['homeInfo']

                if li_dict:
                    address = li_dict['streetAddress'] + li_dict['zipcode']
                    price = li_dict['price']
                    beds = int(li_dict['bedrooms'])
                    baths = int(li_dict['bathrooms'])
                    lat = float(li_dict['latitude'])
                    long = float(li_dict['longitude'])
                    neighborhood_string = neighborhood
                    today = date.today()

                    neighborhood_list.append([address, price, beds, baths, neighborhood_string, lat, long, today])
                 
            except Exception as e:
            # handle the exception accordingly
                pass
        return neighborhood_list
    
    def cleanUpNeighborhood(self, neighborhoods):
        columns = ['Address', 'Price', 'Beds', 'Baths', 'Neighborhood','Latitude','Longitude','Date_Webscraped']
        cleaned_df = pd.DataFrame(neighborhoods, columns = columns)
        return cleaned_df
    
    def writeToCSV(self, df):
        today = df['Date_Webscraped'].iloc[-1]
        zillow_path = './zillow_files/apartments_scraped_{}'.format(today)
        df.to_csv(zillow_path)



if __name__ == "__main__":
    zillow = ZillowScraper()
    fishtown_page = zillow.getUrl("fishtown")
    fishtown_list = zillow.extractData(fishtown_page,"Fishtown")

    fairmount_page = zillow.getUrl("fairmount")
    fairmount_list = zillow.extractData(fairmount_page,"Fairmount")

    passyunk_page = zillow.getUrl("passyunk_square")
    passyunk_list = zillow.extractData(passyunk_page,"Passyunk Square")

    rittenhouse_page = zillow.getUrl("rittenhouse")
    rittenhouse_list = zillow.extractData(rittenhouse_page,"Rittenhouse")

    final_df = zillow.cleanUpNeighborhood([*fishtown_list,*fairmount_list,\
                                            *passyunk_list,*rittenhouse_list])
    
    zillow.writeToCSV(final_df)
    

