import requests
from bs4 import BeautifulSoup


def crawl():
    try:
        url = 'https://bdchan.com/'
    except KeyError:
        return ['site down mone e hoi  :( ']
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'xml')
    half_links = soup.find_all(class_="latest-thread-anchor")
    unique_half_links = []
    counter = 0
    for link in half_links:
        if link['href'] not in unique_half_links:
            unique_half_links.append(link['href'])
            counter += 1
        if counter > 5:
            break
    full_links = ['https://bdchan.com' + link for link in unique_half_links]
    return full_links
