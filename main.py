from bs4 import BeautifulSoup
import requests
import pandas
from urllib.parse import urljoin
from urllib.request import urlopen

# Category Page - https://en.wikipedia.org/wiki/Category:Naval_battles_of_World_War_II_involving_the_United_States
# Category Page - https://en.wikipedia.org/wiki/Category:Battles_of_World_War_II_involving_the_United_States
# Category Page - https://en.wikipedia.org/wiki/Category:Amphibious_operations_involving_the_United_States
# Battle Page - https://en.wikipedia.org/wiki/Battle_of_Midway

def return_historic_date(soup):
    try:
        elem = soup(text='Date')
        parentparent = elem[0].parent.parent
        x = parentparent.find_all('td')
        return x[0].text
    except:
        return 'No Date'

def return_geo_info(soup):
    try:
        a = soup.find('span', {'class':'geo'})
        if a is None:
            return 'No Location'
        b = a.text.split(';')
        return b
    except:
        return 'No Location'

def return_website_soup(url):
    # Headers are not needed but will greatly increase chances of success and not getting blocked. 
    headers = {
    'User-Agent': 'My User Agent 1.0',
    'From': 'anotherEmailAddress@gmail.com'  
    }
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    return soup

def return_title(soup):
    # Find will use the actual HTML title. In this case, TITLE is an html title in the head section
    a = soup.find('title')
    return str.replace(a.text,  ' - Wikipedia','')

def run_single_page_example():
    # This example gets us the sites title and date of event. 
    soup = return_website_soup("https://en.wikipedia.org/wiki/Battle_of_Midway")
    print(return_title(soup))
    print(return_historic_date(soup))

if __name__ == "__main__":


    start_url = "https://en.wikipedia.org/wiki/Category:Naval_battles_of_World_War_II_involving_the_United_States"
    soup = return_website_soup(start_url)

    for ul in soup.find_all('div', {'id':'mw-pages'}): #find every category
        for li in ul.find_all('li'):
            a = li.find('a')
            url2 = urljoin(start_url, a['href'])
            soup2 = BeautifulSoup(urlopen(url2))
            print('***********************')
            print(url2)
            print(return_title(soup2))
            print(return_historic_date(soup2))
            print(return_geo_info(soup2))