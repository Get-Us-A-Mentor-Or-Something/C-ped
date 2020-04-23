import requests
from bs4 import BeautifulSoup
import collections


def search(q='python search'):
    # формування запиту
    q = '%20'.join(q.split())
    url = 'https://stackoverflow.com/search?tab=Relevance&pagesize=50&q=' + q
    req = requests.get(url)
    # отримання блоку з посиланнями на відповіді
    soup = BeautifulSoup(req.content, 'html.parser')
    result_div = soup.findAll(
        'div', attrs={'class': 'question-summary search-result'})
    # тут має бути пошук по декільком сторінкам, якщо вони існують
    # pages = soup.find('div', attrs={'class':})

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
    all_code = collections.defaultdict(list)
    for i in range(len(question_link)):
        code_from_url = []
        requiredHtml = requests.get(question_link[i])
        soup = BeautifulSoup(requiredHtml.content, 'html.parser')
        for data in soup.findAll('pre'):
            for values in data.findAll('code'):
                code_from_url.append(values.text)
        all_code[question_link[i]].append(code_from_url)
    return all_code


print(search())
