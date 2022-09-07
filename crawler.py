import requests
from bs4 import BeautifulSoup


dic = {
    'bangladesh': 'https://news.google.com/rss/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNREUyTW1JU0FtSnVLQUFQAQ?hl=bn&gl=BD&ceid=BD%3Abn',
    'world': 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtSnVHZ0pDUkNnQVAB?hl=bn&gl=BD&ceid=BD%3Abn',
    'sports': 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FtSnVHZ0pDUkNnQVAB?hl=bn&gl=BD&ceid=BD%3Abn',
    'pori_moni': 'https://news.google.com/rss/topics/CAAqJAgKIh5DQkFTRUFvS0wyMHZNRjluZDNkc05CSUNZbTRvQUFQAQ?hl=bn&gl=BD&ceid=BD%3Abn'
}


def crawl(topic):
    try:
        url = dic[topic]
    except KeyError:
        return ['ei topic er kono khobor apatoto rakhi nai :(']
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'xml')
    links = soup.find_all('link')
    return links[1:6]
