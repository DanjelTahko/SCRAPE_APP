from bs4 import BeautifulSoup
from urllib.parse import quote
import copy
import pandas as pd
import requests 
from datetime import datetime 

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
        self.word = ""
        self.url = ""
        self.error = False
        self.done = False

    def searchThread(self, word) -> None:
        self.error = False
        self.total_companys = '-'
        self.total_pages    = '-'
        url = self.searchIndustry(word)
        self.scrapeSearch(url)

    def searchIndustry(self, word:str) -> str:
        self.word = word
        self.url =  f"https://www.hitta.se/sök?vad={quote(word)}&riks=1"
        return self.url

    def scrapeSearch(self, url:str) -> None:
        
        self.error = False
        soup = self.returnSoup(url)

        try:
            # Tries to get number of companies and pages
            self.companys = soup.find('span', {'class': 'spacing__left--sm text-nowrap text--normal style_tabNumbers__VbAE7'}).text
            company_to_int = int(self.companys.replace(',', ''))
            get_pages = lambda c : int(c/25) + 1 if (c % 25 > 0) else int(c/25)
            self.total_pages = get_pages(company_to_int)
            self.total_companys = company_to_int

        except (AttributeError, TypeError):
            # If no internet connection
            if (soup == 'ERROR'):
                self.total_companys = None
                self.total_pages = None
            # If other error e.g can't find anything with given search
            else:
                self.total_companys = 0
                self.total_pages = 0

    def returnSoup(self, url:str) -> BeautifulSoup:

        try:
            # Tries to get response from url 
            response = requests.request('GET', url, headers=self.headers, timeout=5.0)
            html = response.text 
            bs = BeautifulSoup(html, 'html.parser')
            return bs

        # No connection or connection related error´
        except requests.exceptions.Timeout:
            self.error = True
            return 'ERROR'
        except requests.exceptions.TooManyRedirects:
            self.error = True
            return 'ERROR'
        except requests.exceptions.RequestException:
            self.error = True
            return 'ERROR'

    def scrapeThread(self, pages:int, filters:list[str], csv:dict) -> None:

        """ Thread to scrape requested pages and remove rows in dataframe according to filters """
        
        self.error = False

        # scrape all pages starting with url 
        companies_dict = self.scrapeMainPage(self.url, pages)

        # if everythings ok, save to /Desktop
        if (not self.error):

            # create dataframe with scraped companies
            dataframe = pd.DataFrame(companies_dict)

            # if theres any filters, drop rows according to filters
            if (len(filters) >= 1):
                dataframe = dataframe.dropna(subset=filters)

            # if theres imported csv to compare, drop duplicate rows
            if (csv != None):
                columns = ['Företag', 'Org-nummer', 'Ort', 'Nummer', 'Hemsida']
                csv_to_compare = pd.read_csv(f"~/Desktop/{csv}")
                # check if imported csv has same structure as scraped csv, otherwise probs not scraped csv
                if (list(csv_to_compare.columns) == columns):
                    df = pd.concat([dataframe, csv_to_compare])
                    dataframe = df.drop_duplicates(keep=False)
                else:
                    print("ERROR - Imported csv does not have columns ['Företag', 'Org-nummer', 'Ort', 'Nummer', 'Hemsida']\nCan't compare and drop duplicates")
            
            # get today date and save csv to /Desktop with todays date
            dt_string = datetime.now().strftime('%Y%m%d')
            dataframe.to_csv(f"~/Desktop/{self.word}-{dt_string}.csv", index=False)
            self.done = True

        self.total_scraped = 0

    def scrapeMainPage(self, url:str, pages:int) -> list[dict]:

        print("started scraping")
        print(f"Pages to scrape : {pages}")

        company_list = []

        for page in range(1, pages+1):
            url = f"{self.url}&typ=ftg&sida={page}"
            print(url)

            soup = self.returnSoup(url)
            if (self.error):
                break

            companys = soup.find_all('a', {'class': 'style_searchResultLink__2i2BY'})
            for c in companys:
                temp_dic = copy.deepcopy(COMPANY_TEMPLATE)
                temp_dic['Företag'] = c.text.strip()
                page = self.scrapeSubPage(f"https://www.hitta.se{c.attrs.get('href')}")
                if (self.error):
                    break
                temp_dic['Org-nummer'] = page['Org-nummer']
                temp_dic['Ort'] = page['Ort']
                temp_dic['Nummer'] = page['Nummer']
                temp_dic['Hemsida'] = page['Hemsida']
                company_list.append(temp_dic)

                self.total_scraped += 1

        print("finished scraping!")
        print(f"Scraped total   : {len(company_list)}")
            
        return company_list

    def scrapeSubPage(self, url:str) -> list[str]:
        """
        Scrapes page with all info about comapny
        * Ort
        * Org-Nummer
        * Nummer (telefon)
        * Hemsida
        """
        
        soup = self.returnSoup(url)
        page_dict = {}

        if (self.error):
            return None

        try:

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
            if (self.error):
                return None
                
            page_dict['Nummer'] = google_dic['Nummer']
            page_dict['Hemsida'] = google_dic['Hemsida']

            return page_dict


        except (AttributeError, TypeError) as e:
            # subpage is industry page with industries , e.g all Interfloras in sweden
            # runs scrapeSubpage again with first in list

            #print(f"Subpage - failed\n{url}\n{e}")
            company = soup.find('a', {'class': 'style_searchResultLink__2i2BY'})
            page = self.scrapeSubPage(f"https://www.hitta.se{company.attrs.get('href')}")
            if (page != None):
                #print(f"- Found the subpage!\n{url}")
                return page
            else:
                #print("- Could not find subpage in subpage..")
                return None

    def googleSearch(self, company_name:str) -> dict:
        """
        Returns website (recommendation | first) & number (if in recommendation)
        """

        google_url = f'https://www.google.com/search?q={quote(company_name)}'
        soup = self.returnSoup(google_url)

        if (self.error):
            return None

        try:
            website = soup.find('a', {'class': 'ab_button'}).attrs.get('href')
            if (website.strip() == '#'):
                website = self.otherWebsiteGoogleSearch(soup)
        except (AttributeError, TypeError):
            # If no recommendation box, take first best search website
            print("could not find website on google recommendation box")
            website = self.otherWebsiteGoogleSearch(soup)

        try:
            number = soup.find('span', {'class', 'LrzXr zdqRlf kno-fv'}).text
        except (AttributeError, TypeError):
            # Returns None if theres no recommendation box
            number = None

        if (website == None):
            # if website not available, write webscraped html to html file
            with open('ERROR.html', 'a') as file:
                file.write(soup)
                self.error = True

        return {'Hemsida': website, 'Nummer': number}

    def otherWebsiteGoogleSearch(self, bs:BeautifulSoup) -> str:
        """
        If google has no recommendation box this method will take first website
        in search and return it as string. If somethings wrong, None will be returned
        """
        if (self.error):
            return None

        try:
            href = bs.select('div.yuRUbf a')[0].attrs.get('href')
            if (href.strip() != '#'):
                return href
            else:
                print("could not find website on google other (else)")
                return None
        except:
            print("could not find website on google other (except)")
            return None

if __name__ == '__main__':
    """for testing"""
    h = Scrape()
    url = h.searchIndustry('inredning')
    h.scrapeSearch(url)
    print(f"Hittade {h.companys} företag på {h.pages} sidor")