from bs4 import BeautifulSoup
from urllib.parse import quote
import copy
import pandas as pd
import requests 
import threading
import time

from settings import *


class Scrape:

    def __init__(self) -> None:
        self.headers = {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Accept-Language' : 'en-US,en;q=0.9',
                    'Connection': 'keep-alive'
                    }
        self.total_companys = '-'
        self.total_pages    = '-'
        self.total_scraped  = 0
        self.url = ""
        self.word = ""

        self.search_thread = threading.Thread(target=self.TEST_search, name="Search")
        self.scrape_thread = threading.Thread(target=self.scrapeMainPage, name="Scrape", args=(self.url,))

    def TEST_search(self, word):
        url = self.searchIndustry(word)
        self.scrapeSearch(url)

    def returnSoup(self, url:str) -> BeautifulSoup:
        try: # är timeout bra? färre / fler försök innan timeout?
            response = requests.request('GET', url, headers=self.headers, timeout=4.0)
            html = response.text 
            bs = BeautifulSoup(html, 'html.parser')
            return bs
        except requests.ConnectionError as e:
            return 'ERROR'

    def searchIndustry(self, word:str) -> str:
        self.url =  f"https://www.hitta.se/sök?vad={quote(word)}&riks=1"
        return self.url

    def scrapeSearch(self, url:str):

        soup = self.returnSoup(url)

        try:
            self.companys = soup.find('span', {'class': 'spacing__left--sm text-nowrap text--normal style_tabNumbers__VbAE7'}).text
            company_to_int = int(self.companys.replace(',', ''))
            get_pages = lambda c : int(c/25) + 1 if (c % 25 > 0) else int(c/25)
            self.total_pages = get_pages(company_to_int)
            self.total_companys = company_to_int
        except (AttributeError, TypeError):

            if (soup == 'ERROR'):
                self.total_companys = None
                self.total_pages = None
            
            else:
                self.total_companys = 0
                self.total_pages = 0

    def scrapeMainPage(self, url:str) -> list[dict]:
        print("started scraping")
        
        soup = self.returnSoup(url)

        company_list = []

        #value = soup.find('span', {'class': 'spacing__left--sm text-nowrap text--normal style_tabNumbers__VbAE7'}).text
        #print(f"Hittade {value} företag.")

        companys = soup.find_all('a', {'class': 'style_searchResultLink__2i2BY'})
        for c in companys:
            temp_dic = copy.deepcopy(COMPANY_TEMPLATE)
            temp_dic['Företag'] = c.text.strip()
            page = self.scrapeSubPage(f"https://www.hitta.se{c.attrs.get('href')}")
            temp_dic['Org-nummer'] = page['Org-nummer']
            temp_dic['Ort'] = page['Ort']
            temp_dic['Nummer'] = page['Nummer']
            temp_dic['Hemsida'] = page['Hemsida']
            company_list.append(temp_dic)

            self.scraped += 1
            
        return company_list

    def scrapeSubPage(self, url:str) -> list[str]:
        
        soup = self.returnSoup(url)

        page_dict = {}

        name = soup.find('h3', {'class': 'style_title__2C92s'}).text

        try:
            page_dict['Ort'] = soup.find('p', {'class': 'text-body-short-sm-semibold spacing--xxs'}).text
        except AttributeError:
             page_dict['Ort'] = None

        try:
            page_dict['Org-nummer'] = soup.find('p', {'class': 'text-caption-md-regular color-text-placeholder'}).text.split(' ')[1]
        except AttributeError:
            page_dict['Org-nummer'] = None

        google_dic = self.googleSearch(name)

        page_dict['Nummer'] = google_dic['Nummer']
        page_dict['Hemsida'] = google_dic['Hemsida']

        return page_dict

    def googleSearch(self, company_name:str) -> dict:
        """
        ### Returns website (recommendation | first) & number (if in recommendation)
        """
        
        google_url = f'https://www.google.com/search?q={quote(company_name)}'
        soup = self.returnSoup(google_url)

        try:
            website = soup.find('a', {'class': 'ab_button'}).attrs.get('href')
            if (website.strip() == '#'):
                website = self.otherWebsiteGoogleSearch(soup)
        except AttributeError:
            website = self.otherWebsiteGoogleSearch(soup)

        try:
            number = soup.find('span', {'class', 'LrzXr zdqRlf kno-fv'}).text
        except AttributeError:
            number = None

        return {'Hemsida': website, 'Nummer': number}

    def otherWebsiteGoogleSearch(self, bs:BeautifulSoup) -> str:

        try:
            href = bs.select('div.yuRUbf a')[0].attrs.get('href')
            if (href.strip() != '#'):
                return href
            else:
                return None
        except:
            return None



if __name__ == '__main__':
    h = Scrape()
    """
    url = h.search('pr kommunikation')
    #print(url)
    ls = h.scrapeMainPage(url)
    df = pd.DataFrame(ls)
    print(df)
    """
    url = h.searchIndustry('inredning')
    h.scrapeSearch(url)
    print(f"Hittade {h.companys} företag på {h.pages} sidor")
    th = threading.Thread(target=h.scrapeMainPage, name="Scrape", args=(url,))
    #th.start()
    i = 1
    while(True):
        print(h.scraped)
        if (i == 1):
            i = 0
            print("starting thread")
            th.start()
            print("finnished thred")

        th.is_alive()
        time.sleep(1)



    
