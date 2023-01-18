import scrapy

class PgaTourSuperstoreSpider(scrapy.Spider):
    name = 'ptsSpider'
    allowed_domains = ['pgatoursuperstore.com']
    start_urls = ['https://www.pgatoursuperstore.com/golf-clubs/drivers/?sz=1000',
                  'https://www.pgatoursuperstore.com/golf-clubs/irons-sets/?sz=1000',
                  'https://www.pgatoursuperstore.com/golf-clubs/putters/?sz=1000',
                  'https://www.pgatoursuperstore.com/golf-clubs/fairway-metals/?sz=1000',
                  'https://www.pgatoursuperstore.com/golf-clubs/hybrids/?sz=1000',
                  'https://www.pgatoursuperstore.com/golf-clubs/wedges/?sz=1000']

    def parse(self, response):
        for link in response.css('div.product-tile a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_club)

    def parse_club(self, response):
        club_name = response.css('h1.product-name::text').get()
        price = response.css('span.price-sales::text').get()
        if price:
            price = price.strip()
        else:
            price = response.css('div.bfx-price::text').get()
            if price:
                price = price.strip()
            else:
                price = 'Not Found'
        link = response.url

        yield {
            'name': club_name.strip(),
            'price': price,
            'link': link
        }