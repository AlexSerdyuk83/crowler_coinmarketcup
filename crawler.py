import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from multiprocessing import Pool


def get_html(url):
    r = requests.get(url)
    
    return r.content  # Returning the html code of the page


def get_all_lincs(html):
    soup = BeautifulSoup(html, 'lxml')

    divs = soup.find_all('div', class_='cmc-table__column-name')

    links = []

    for div in divs:
        a = div.find('a').get('href') # string
        link = 'https://coinmarketcap.com' + a
        links.append(link)

    return links


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    try:
        name = soup.find('h1').text.strip()
    except:
        name = ''
    try:
        price = soup.find('span', class_='cmc-details-panel-price__price').text.strip()
    except:
        price = ''
    data = {'name': name, 'price': price}
    return data


def write_csv(data):
    with open('coinmarketcup.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow((data['name'], data['price']))

        print(data['name'], 'parsed')


def make_all(url):
    html = get_html(url)
    data = get_page_data(html)
    write_csv(data)


def main():
    start = datetime.now()

    url = 'https://coinmarketcap.com/all/views/all/'
    all_links = get_all_lincs( get_html(url) )

    # for urls in all_links:
    #    html = get_html(urls)
    #    data = get_page_data(html)
    #    write_csv(data)

    with Pool(40) as p:
        p.map(make_all, all_links)

    end = datetime.now()

    total = end - start
    print(str(total))


if __name__ == "__main__":
    main()