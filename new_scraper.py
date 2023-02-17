from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests as rt

# NASA Exoplanet URL
START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"

# Webdriver
browser = webdriver.Chrome("D:/Setup/chromedriver_win32/chromedriver.exe")
browser.get(START_URL)

time.sleep(10)
headers = ["name","light_years_from_earth","planet_mass","stellar_magnitude","discovery_date","hyperlink","planet_type","planet_radius","orbital_radius","orbital_period","eccentricity"]
planets_data = []
new_planet_data =[]

def scrape_more_data(hyperlink):
    try:
        page = rt.get(hyperlink)
        soup = BeautifulSoup(page.content,"html.parser")
        temp_list = []
        for tr_tag in soup.find_all("tr",attrs = {"class" : "fact_row"}):
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div",attrs = {"class" : "value"})[0].contents[0])
                except:
                    temp_list.append("")
        new_planet_data.append(temp_list)
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)

planet_df_1 = pd.read_csv("updated_scraped_data.csv")

for index,row in planet_df_1.iterrows():
    print(row["hyperlink"])
    scrape_more_data(row["hyperlink"])
    print(f"data scraping at hyperlink {index + 1} completed")

scrapped_data = []
for row in new_planet_data:
    replaced = []
    for el in row:
        el = el.replace("\n","")
        replaced.append(el)
    scrapped_data.append(replaced)
    
print(scrapped_data)

        
# Define pandas DataFrame 
new_planet_df_1 = pd.DataFrame(scrapped_data, columns=headers)

# Convert to CSV
new_planet_df_1.to_csv('new_scraped_data.csv',index=True, index_label="id")