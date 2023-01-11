import scrapy

class CallawaySpider(scrapy.Spider):
    name = 'callawaySpider'
    allowed_domains = ['callawaygolf.com']
    start_urls = ['https://www.callawaygolf.com/golf-clubs/drivers/',
                  'https://www.callawaygolf.com/golf-clubs/fairway-woods/',
                  'https://www.callawaygolf.com/golf-clubs/iron-sets/',
                  'https://www.callawaygolf.com/golf-clubs/hybrids/',
                  'https://www.callawaygolf.com/golf-clubs/wedges/',
                  'https://www.callawaygolf.com/tour-limited/',
                  'https://www.callawaygolf.com/clubs/womens/'
    ]

    def parse(self, response):
        for link in response.css('div.product-tile a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_club)

    def parse_club(self, response):
        club_name = response.css('h1::text').get()
        price = response.css('span.adjusted::text').get()
        if type(price) == str:
            price = price.strip()
        link = response.url

        yield {
            'name': club_name,
            'price': price,
            'link': link
        }