import scrapy

class TitleistSpider(scrapy.Spider):
    name = 'titleistSpider'
    allowed_domains = ['titleist.com']
    start_urls = ['https://www.titleist.com/golf-clubs/']

    def parse(self, response):
        for link in response.css('div.product-tile-details a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_club)

    def parse_club(self, response):
        club_name = response.css('h1.product-name::text').get()
        price = response.css('span.price-sales::text').get()
        link = response.url

        yield {
            'name': club_name.strip(),
            'price': price.strip(),
            'link': link
        }