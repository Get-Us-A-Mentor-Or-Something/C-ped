import requests
from bs4 import BeautifulSoup
import collections


def make_query(q=None, tags=None, is_accepted=False, tab = 'Relevance', pagesize = 50):
    # формування запиту
    url = 'https://stackoverflow.com/search?'
    query = url + '&tab=' + tab + '&pagesize=' + str(pagesize) + '&q='
    if q:
        sep = '+'
        q = sep.join(q.split())
        query = query + q
    if tags:
        sep = ['+%5B', '%5D']
        tags = tags.replace('[', sep[0]).replace(']', sep[1])
        query = query + tags
    if is_accepted:
        query = query + '+isaccepted:yes'
    return query


def search(quarry, n):
    all_code = []
    page = 1
    try:
        for i in range(n):
            quarry_page = quarry + '&page='+str(page)
            req = requests.get(quarry)
            # отримання блоку з посиланнями на відповіді
            soup = BeautifulSoup(req.content, 'html.parser')
            result_div = soup.findAll(
                'div', attrs={'class': 'question-summary search-result'})

            # отримання посилань на відповіді
            question_link = []
            for r in result_div:
                # перевірка на те чи елемент присутній
                try:
                    link = r.find('a', href=True)
                    if link != '':
                        question_link.append(
                            'https://stackoverflow.com/' + link['href'])
                except:
                    continue

            # парсинг коду з сторінки
            for i in range(len(question_link)):
                code_from_url = []
                requiredHtml = requests.get(question_link[i])
                soup = BeautifulSoup(requiredHtml.content, 'html.parser')
                for data in soup.findAll('pre'):
                    for values in data.findAll('code'):
                        code_from_url.append(values.text)
                result_obj = {}
                result_obj["href"] = question_link[i]
                result_obj["code"] = [] + code_from_url
                result_obj["date"] = soup.find('time').text
                result_obj["likes"] = min(
                    abs(i**2 - i * 3), abs(i - i**3)) % 20
                result_obj["text"] = soup.find(
                    'a', attrs={'class': 'question-hyperlink'}).text

                all_code.append(result_obj)
            page += 1
            return all_code
    except:
        raise ValueError


def search_dynamic(quarry, n, client):
    page = 1
    try:
        for i in range(n):
            quarry_page = quarry + '&page='+str(page)
            req = requests.get(quarry)
            # отримання блоку з посиланнями на відповіді
            soup = BeautifulSoup(req.content, 'html.parser')
            result_div = soup.findAll(
                'div', attrs={'class': 'question-summary search-result'})

            # отримання посилань на відповіді
            question_link = []
            for r in result_div:
                # перевірка на те чи елемент присутній
                try:
                    link = r.find('a', href=True)
                    if link != '':
                        question_link.append(
                            'https://stackoverflow.com/' + link['href'])
                except:
                    continue

            # парсинг коду з сторінки
            for i in range(len(question_link)):
                code_from_url = []
                requiredHtml = requests.get(question_link[i])
                soup = BeautifulSoup(requiredHtml.content, 'html.parser')
                for data in soup.findAll('pre'):
                    for values in data.findAll('code'):
                        code_from_url.append(values.text)
                result_obj = {}
                result_obj["href"] = question_link[i]
                result_obj["code"] = [] + code_from_url
                result_obj["date"] = soup.find('time').text
                result_obj["likes"] = min(
                    abs(i**2 - i * 3), abs(i - i**3)) % 20
                result_obj["text"] = soup.find(
                    'a', attrs={'class': 'question-hyperlink'}).text

                client.add_result(result_obj)
            page += 1
    except:
        raise ValueError
