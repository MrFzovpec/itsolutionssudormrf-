import requests
from bs4 import BeautifulSoup as bs

headers = {'accept': '*/*',
                'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}

base_url = 'https://info.olimpiada.ru/activities'
def hh_parse(base_url, headers):
    session = requests.Session()
    request = session.get(base_url,headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        divs = soup.find_all('td')
        for div in divs:
            title = div.find('a', attrs={'class': 'black_hover_blue'}).text
            href = div.find('a', attrs={'class': 'black_hover_blue'})["href"]
            print(title)
            print(href)
    else:
        print("JOPA")

hh_parse(base_url, headers)
