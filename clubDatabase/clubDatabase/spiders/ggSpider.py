import scrapy

class GolfGalaxySpider(scrapy.Spider):
    name = 'ggSpider'
    allowed_domains = ['golfgalaxy.com']
    start_urls = ['https://www.golfgalaxy.com/f/golf-clubs-and-golf-club-sets?pageSize=144']

    def parse(self, response):
        for link in response.css('div.rs_product_card a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_club)

    def parse_club(self, response):
        club_name = response.css('h1.title::text').get()
        price = response.css('span.product-price::text').get()
        if price:
            price = price.strip()
        priceMax = response.css('div.product-price-max::text').get()
        if priceMax:
            priceMax = priceMax.strip()
            price = price + ' - ' + priceMax
        if not price:
            price = 'Not Found'
            
        link = response.url

        yield {
            'name': club_name.strip(),
            'price': price,
            'link': link
        }