# импорт библиотек
import requests
from bs4 import BeautifulSoup as bs
import csv

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}


# указываем ссылку на сайт
base_url = 'https://olimpiada.ru/activities'
# основаня функция



def ol_parse(base_url, headers):
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    full = []
    # делаем запрос
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        divs_2 = soup.find_all('div', attrs={'class': 'tl_event long'})
        divs = soup.find_all('div', attrs={'class': 'fav_olimp olimpiada'})
        # достаем дату
        for div in divs_2:
            date = div.find('span', attrs={'class': 'tl_cont_s'}).text
            print(date)
            full.append({
            'date': date
            })

        # достаем ссылку название рейтинг и класс
        for div in divs:

            title = div.find('span', attrs={'class': 'headline'}).text
            href = div.find('a', attrs={'class': 'none_a black'})["href"]
            classes = div.find('span', attrs={'class': 'classes_dop'}).text
            rait = div.find('span', attrs={'class': 'pl_rating'}).text

            full.append({
                'title': title,
                'href': "https://olimpiada.ru" + href,
                'classes': classes,
                'rait': rait
            })
        for i in range(0, len(full)):
            print(full[i])
    # если не подключились
    else:
        print("NEOK")
    return full

def file_writer(full):
    with open('olymp.csv', 'a') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('Название олимпиады', 'ссылка', 'класс', 'Рейтинг', 'Дата'))
        for ful in full:
            a_pen.writerow((full['title'], full['href'], full['classes'], full['rait'], full['date']))


<<<<<<< HEAD

# вызываем функцию
ol_parse(base_url, headers)
=======
#вызываем функцию
full =  ol_parse(base_url, headers)
file_writer(full)
>>>>>>> 7483aa70b3fb54e6d74d3b6a4dcc89c8d5a24588
