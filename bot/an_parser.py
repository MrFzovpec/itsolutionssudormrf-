#импорт библиотек
import requests
from bs4 import BeautifulSoup as bs


headers = {'accept': '*/*',
                'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}


#указываем ссылку на сайт
base_url = 'https://hh.ru/search/vacancy?area=1&st=searchVacancy&text=Java'
#основаня функция
def ol_parse(base_url, headers):
    session = requests.Session()
    request = session.get(base_url,headers=headers)
    jobs = []
    #делаем запрос
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        divs = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})

        for div in divs:
            title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
            href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})["href"]
            company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
            disc_1 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
            disc_2 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
            disc = disc_1 + ' ' + disc_2
            jobs.append({
                'title': title,
                'href': href,
                'company': company,
                'disc': disc
            })
        for i in range(0,len(jobs)):
            print(jobs[i])
            i+=1
        print(len(jobs))

        #достаем дату

        #достаем ссылку название рейтинг и класс
        #for div in divs:

            #title = div.find('h2', attrs={'class': 'event__name'}).text
            #org = div.find('div', attrs={'class': 'event__description-value'}).text
            #href = div.find('a', attrs={'class': 'event__name-link'})["href"]
            #classes = div.find('div', attrs={'class': 'event__description-value'}).text
            #rait = div.find('span', attrs={'class': 'pl_rating'}).text


            #print(org)
            #print("https://olimpiada.ru"+href)
            #print(classes)
            #print(rait)
    #если не подключились
    else:
        print("NEOK")

#вызываем функцию
ol_parse(base_url, headers)
