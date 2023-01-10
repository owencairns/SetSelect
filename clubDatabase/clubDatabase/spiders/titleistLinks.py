import scrapy
from scrapy.exporters import JsonItemExporter
from bs4 import BeautifulSoup

class TitleistClubLinks(scrapy.Spider):
    name = 'titleistLinks'
    start_urls = ['https://www.titleist.com/golf-clubs']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')

        for product in soup.find_all('div', class_='product-tile-details'):
            #name = product.find('a').text
            #price = product.find('span', class_='product-sale-price').text
            #category = product.find('div', class_='product-category').text
            link = product.find('a')['href']

            yield {
                #'name': name.strip(),
                #'category': category.strip(),
                #'price': price.strip(),
                'link': 'https://www.titleist.com' + link.strip()
            }