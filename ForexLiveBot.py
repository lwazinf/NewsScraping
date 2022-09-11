from pandas import pandas as pd
from bs4 import BeautifulSoup as bs4
import urllib.request
import re

page_ = 1
df = pd.DataFrame(columns=['time', 'day', 'date', 'month', 'year', 'type', 'brief', 'body'])
remove_lower = lambda text: re.sub('[a-z]', '', text)
def newEntry(index_):
    global df
    df = pd.concat([
        df,
        pd.DataFrame({
        'time': [data[index_].find_all('div', {'class': 'publisher-details__date'})[0].text.replace('\n', '').replace(' ', '').replace('|', ',').split(',')[2][0:5]],
        'day': [data[index_].find_all('div', {'class': 'publisher-details__date'})[0].text.replace('\n', '').replace(' ', '').replace('|', ',').split(',')[0][0:3]],
        'date': [data[index_].find_all('div', {'class': 'publisher-details__date'})[0].text.replace('\n', '').replace(' ', '').replace('|', ',').split(',')[1].split('/')[0]],
        'month': [data[index_].find_all('div', {'class': 'publisher-details__date'})[0].text.replace('\n', '').replace(' ', '').replace('|', ',').split(',')[1].split('/')[1]],
        'year': [data[index_].find_all('div', {'class': 'publisher-details__date'})[0].text.replace('\n', '').replace(' ', '').replace('|', ',').split(',')[1].split('/')[2]], 'timezone': [data[index_].find_all('div', {'class': 'publisher-details__date'})[0].text.replace('\n', '').split(' ')[
        data[index_].find_all('div', {'class': 'publisher-details__date'})[0].text.replace('\n', '').split(' ').index("|") + 2
        ]],
        'type': [remove_lower(data[index_].find_all('a', {'class': 'article-header__category-section'})[0].text.replace('\n', '').replace(' ', ''))],
        'brief': [data[index_].find_all('div', {'class': 'article-slot__wrapper'})[0].attrs['brief']],
        'body': [data[index_].find_all('li', {'class': 'text-body'})[0].text.replace('\n', '')]
        })
    ], ignore_index=True)

    return df

# while len(df.index) < 10:
for i in range(5):
    global page_

    source = urllib.request.urlopen(f'https://www.forexlive.com/page/{page_}').read()
    soup = bs4(source, 'html.parser')
    data = soup.find_all("div", {"class": "article-list__item-wrapper"})
    for x in range(len(data)):
        # print(x)
        # print(page_)
        # print(range(len(data)))
        #
        # a = 'nasdaq' in data[x].find_all('li', {'class': 'text-body'})[0].text.replace('\n', '').lower()
        # a_ = 'nasdaq' in data[x].find_all('div', {'class': 'article-slot__wrapper'})[0].attrs['brief']
        #
        # if (a or a_):
        newEntry(x)

    page_ = page_+1



len(df.index)
