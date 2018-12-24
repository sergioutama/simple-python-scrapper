import requests
import random
import re
import json
import csv
from bs4 import BeautifulSoup
from scraputil import *

# 'https://myfave.com/sitemap.xml'
def scrap_main_sitemaps(url):
    print("scrapping page:",url)
    headers = {
        'user-agent': random_user_agent(),
    }

    response = requests.get(url,headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')

        for partner_sitemap_url in soup.find_all('loc'):
            print(partner_sitemap_url)
            if 'partners.xml' in partner_sitemap_url.text:
                scrap_partner_sitemap(partner_sitemap_url.text)


def scrap_partner_sitemap(url):
    print("scrapping page:",url)
    headers = {
        'user-agent': random_user_agent(),
    }
    response = requests.get(url,headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        
        csv_writter = csv.writer(open('{}.csv'.format(url),'w'),delimiter='|',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writter.writerow([
            "company name",
            "company website",
            "company description",
            "outlet name",
            "outlet active",
            "outlet email",
            "outlet phone",
            "outlet address"])
            
        for partner_url in soup.find_all('loc'):
            # get all the data required
            partner_data = scrap_partner_page(partner_url.text)
            write_to_csv(csv_writter,partner_data,partner_url.text)


def scrap_partner_page(url):
    print("scrapping page:",url)
    headers = {
        'user-agent': random_user_agent(),
    }
    response = requests.get(url,headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        partner_data = scrap_partner_data(soup)
        return partner_data
    else:
        print(response.status_code)
        return {"error":"failed to connect to server"}

def scrap_partner_data(soup):
    print("scrapping partner data")
    partner_json = partner_json_builder(soup)
    outlets_json = outlets_json_builder(soup)
    json_text = '{{{},{}}}'.format(partner_json,outlets_json)
    try:
        json_data = json.loads(json_text)    
        return json_data
    except :
        return {"error":"malformatted json"}
    

def write_to_csv(csv_writter, json_data, scrap_url):
    if "error" in json_data:
        csv_writter.writerow([
            scrap_url,
            "error getting this data",
            "",
            "",
            "",
            "",
            "",
            "",
            ])
        return
    
    if len(json_data["outlets"]) < 1:
        csv_writter.writerow([
            json_data.get('partnersObj',{}).get('name',""),
            json_data.get('partnersObj',{}).get('website',""),
            json_data.get('partnersObj',{}).get('description',""),
            "",
            "",
            "",
            "",
            "",
            ])
        return

    for outlet in json_data["outlets"]:
        csv_writter.writerow([
            json_data.get('partnersObj',{}).get('name',""),
            json_data.get('partnersObj',{}).get('website',""),
            json_data.get('partnersObj',{}).get('description',""),
            outlet.get("name",""),
            outlet.get("active","false"),
            outlet.get("email",""),
            outlet.get("telephone",""),
            outlet.get("address","")
            ])
        return
        
