from bs4 import BeautifulSoup
import numpy as np
import requests

def parse_url_text(i):
    url=f'https://www.airlinequality.com/airline-reviews/british-airways/page/{i}/'
    page=requests.get(url).text
    soup=BeautifulSoup(page,'html.parser')
    articles=soup.find_all('article',{'itemprop':'review'})
    return articles

def value_fetcher(soup, headers_text, fields_text, headers_star, fields_star):
    # append nan value in case the feature has an empty customer rating
    for i in range(len(headers_text)):
        fields_text[i].append(np.nan)
    for i in range(len(headers_star)):
        fields_star[i].append(np.nan)

    # loop through all rows of type 'tr' in soup    
    for row in soup.find_all('tr'):
        # finds header and value of comment field
        header=row.find('td', class_ = 'review-rating-header').text
        value=row.find('td', class_ = 'review-value')
        # loop through text ratings
        for i in range(len(headers_text)):
            if header == headers_text[i]:
                fields_text[i][-1] = value.text
        # loop through star ratings
        for i in range(len(headers_star)):
            if header == headers_star[i]:
                fields_star[i][-1] = len(row.find_all('span', class_ = 'star fill'))

def rating_fetcher(article):
    if article.find('span',{'itemprop':'ratingValue'}):
        rating_value = article.find('span',{'itemprop':'ratingValue'}).text
    else:
        rating_value = np.nan
    return rating_value

def review_fetcher(div):
    content = div.find('div', class_ = 'text_content').text.split('|')
    if len(content) == 2:
        verification, review = content
    else:
        verification = np.nan
        review = content[0]
    return verification, review