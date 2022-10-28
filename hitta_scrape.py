from bs4 import BeautifulSoup
from urllib.parse import quote
import requests 


class HittaScrape:

    def __init__(self) -> None:
        self.headers = {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Accept-Language' : 'en-US,en;q=0.9',
                    'Connection': 'keep-alive'
                    }

    def returnSoup(self, url:str) -> BeautifulSoup:
        response = requests.request('GET', url, headers=self.headers)
        html = response.text 
        bs = BeautifulSoup(html, 'html.parser')
        return bs

    def search(self, word:str) -> str:
        return f"https://www.hitta.se/sök?vad={quote(word)}&riks=1"

    def scrapeMainPage(self, url:str) -> None:
        
        soup = self.returnSoup(url)


        value = soup.find('span', {'class': 'spacing__left--sm text-nowrap text--normal style_tabNumbers__VbAE7'}).text
        print(f"Hittade {value} företag.")

        companys = soup.find_all('a', {'class': 'style_searchResultLink__2i2BY'})
        for c in companys:
            print(c.text)

    def scrapeSubPage(self):
        pass

    def googleSearch(self, company_name:str):
        
        google_url = f'https://www.google.com/search?q={quote(company_name)}'
        soup = self.returnSoup(google_url)

        # frame to the right for best result
        name = 'h2.qrShPb kno-ecr-pt PZPZlf q8U8x hNKfZe'
        website = 'a.ab_button' #href
        number = 'span.LrzXr zdqRlf kno-fv"'

        # links in search field
        url_ = soup.find('div', {'class': 'yuRUbf'})
        print(url_.text)


    """
    google    = 0662512140
    allabolag = 066230270

    https://www.google.com/search?q=PMI%20Hotell%20Interi%C3%B6r
    """







if __name__ == '__main__':
    h = HittaScrape()
    url = h.search('Konferenslokaler')
    print(url)
    #h.scrapePage(url)

"""
TODO :
    Scrapea alla brancher och lägg in dem så man kan välja via kategori om man vill
    https://www.hitta.se/sitemap/branscher

https://www.hitta.se/kassask%C3%A5p+stockholm/f%C3%B6retag/2
https://www.hitta.se/kassaskåp+stockholm/företag/2

"""