#https://www.linkedin.com/jobs/search?keywords=python&location=Dhaka%2C%20Bangladesh&geoId=103363366&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0
import requests
from bs4 import BeautifulSoup


def crawl(keywords):
    url = f'https://www.linkedin.com/jobs/search?keywords={keywords}&location=Dhaka%2C%20Bangladesh&geoId=103363366&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'xml')
    cards = soup.find_all('div', class_='base-card')
    positions = []
    urls = []
    for card in cards:
        position = card.find('span', class_='sr-only')
        url = card.find('a', class_='base-card__full-link')
        positions.append(position.get_text(strip=True))
        urls.append(url['href'])
    return positions, urls



