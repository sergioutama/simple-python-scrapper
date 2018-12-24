from bs4 import BeautifulSoup
import random
import re

def random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.39 (KHTML, like Gecko) Version/9.0 Safari/601.1.39',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.38 Safari/537.36'
        ]

    random_index = random.randint(0,len(user_agents)-1)
    return user_agents[random_index]
    
def soup_text(soup, default_text = ""):
    if soup:
        return soup.text
    else:
        return default_text

def partner_json_builder(soup):
    partner_name = soup.find('h3',class_='partner-name')
    for child in partner_name.find_all('div'):
        child.decompose()
    partner_name_text = soup_text(partner_name)

    partner_desc = soup.find('div',class_='full-text')
    partner_desc_text = soup_text(partner_desc)

    partner_link = soup.find('a',class_='external-link')
    partner_link_text = "" if partner_link is None else partner_link['href']

    # get from react
    partnersObj_matches = re.findall(r'partnersObj: (.*),\s',soup.text)

    if len(partnersObj_matches)>0:
        result = '"partnersObj":{}'.format(partnersObj_matches[0])
        print('partner_json_builder | has partner')
        print(result)
        return result
    else:
        result = '"partnersObj":{{"name":"{}","description":"{}","website":"{}"}}'.format(partner_name_text,partner_desc_text,partner_link_text)
        print('partner_json_builder')
        print(result)
        return result


def outlets_json_builder(soup):
    outlets_matches = re.findall(r'outlets: (.*)\s',soup.text)
    if len(outlets_matches)>0:
        result = '"outlets":{}'.format(outlets_matches[0])
        print('outlet_json_builder | has outlet')
        print(result)
        return result
    else:
        result = '"outlets":{}'.format(outlets_matches)
        print('outlet_json_builder')
        print(result)
        return result