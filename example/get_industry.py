from bs4 import BeautifulSoup
import requests


def getSoup(url) -> BeautifulSoup:
    headers = {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Accept-Language' : 'en-US,en;q=0.9',
                    'Connection': 'keep-alive'
                    }
    response = requests.request('GET', url, headers=headers)
    html = response.text
    bs = BeautifulSoup(html, 'html.parser')
    return bs 


def hitta(url) -> dict:
    soup = getSoup(url)
    ul_tag = soup.find('ul')
    industries = ul_tag.select('li') 
    tempdict = {}
    for industry in industries:
        if ('län' not in industry.text):
            sub_url = f"https://www.hitta.se{industry.find('a').attrs.get('href')}"
            tempdict[industry.text] = hitta(sub_url)
            print(industry.text)
        else:
            break
    return tempdict
    


print(hitta('https://www.hitta.se/sitemap'))