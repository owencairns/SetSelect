import scrapy

class PgaTourSuperstoreSpider(scrapy.Spider):
    name = 'ptsSpider'
    allowed_domains = ['pgatoursuperstore.com']
    start_urls = ['https://www.pgatoursuperstore.com/golf-clubs/drivers/?start=0&sz=11&format=page-element',
                  'https://www.pgatoursuperstore.com/golf-clubs/irons-sets/?start=0&sz=11&format=page-element',
                  'https://www.pgatoursuperstore.com/golf-clubs/putters/?start=0&sz=11&format=page-element',
                  'https://www.pgatoursuperstore.com/golf-clubs/fairway-metals/?start=0&sz=11&format=page-element',
                  'https://www.pgatoursuperstore.com/golf-clubs/hybrids/?start=0&sz=11&format=page-element',
                  'https://www.pgatoursuperstore.com/golf-clubs/wedges/?start=0&sz=11&format=page-element',
                  'https://www.pgatoursuperstore.com/golf-clubs/completesets/?start=0&sz=11&format=page-element',
                  'https://www.pgatoursuperstore.com/golf-clubs-womensclubs/?start=0&sz=11&format=page-element']
    
    def parse(self, response):
        for link in response.css('div.product-tile a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_club)
        next = response.css('a.infinite-scroll-loader::attr(data-grid-url)').get()
        if not next:
            next = response.css('a.infinite-scroll-placeholder::attr(data-grid-url)').get()
        if next:
            yield response.follow(next, callback=self.parse)

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