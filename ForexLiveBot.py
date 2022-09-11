from pandas import pandas as pd
from bs4 import BeautifulSoup as bs4
import urllib.request
import re

source = urllib.request.urlopen('https://www.forexlive.com/page/2').read()
soup = bs4(source, 'html.parser')

data = soup.find_all("div", {"class": "article-list__item-wrapper"})

remove_lower = lambda text: re.sub('[a-z]', '', text)

df = pd.DataFrame(columns=['time', 'day', 'date', 'month', 'year', 'type', 'brief', 'body'])

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

newEntry(0)
