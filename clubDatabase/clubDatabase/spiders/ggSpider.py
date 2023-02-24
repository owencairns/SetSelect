import scrapy
import json

class GolfGalaxySpider(scrapy.Spider):
    name = 'ggSpider'
    start_urls = ['https://www.golfgalaxy.com/f/golf-clubs-and-golf-club-sets']

    def parse(self, response):
        num_products = response.css('span.rs-page-count-label::text').getall()
        num_products = num_products[1].split()
        total = int(num_products[0])
        url = 'https://prod-catalog-product-api.dickssportinggoods.com/v2/search?searchVO=%7B%22selectedCategory%22%3A%2210051_76724%22%2C%22selectedStore%22%3A%22420%22%2C%22selectedSort%22%3A5%2C%22selectedFilters%22%3A%7B%7D%2C%22storeId%22%3A10701%2C%22pageNumber%22%3A{}%2C%22pageSize%22%3A144%2C%22totalCount%22%3A{}%2C%22searchTypes%22%3A%5B%22PINNING%22%5D%2C%22isFamilyPage%22%3Atrue%2C%22snbAudience%22%3A%22%22%7D'
        for i in range(int(total/144) + 1):
            yield response.follow(url.format(i, total), self.parse_json)

    def parse_json(self, response):
        data = json.loads(response.text)
        products = data['productVOs']
        for product in products:    
            link = 'https://www.golfgalaxy.com/' + product['assetSeoUrl']
            yield response.follow(link, self.parse_club)
    
    def parse_club(self, response):
        club_name = response.css('h1.title::text').get()
        if club_name:
            club_name = club_name.strip()
        price = response.css('span.product-price::text').get()
        if price:
            price = price.strip()
        max_price = response.css('span.product-price-max::text').get()
        if max_price:
            max_price.strip()
            price = price + '-' + max_price
        link = response.url
        condition = 'new'
        if ('used' or 'Used') in club_name:
            condition = 'used'
        if 'driver' in club_name.lower():
            club_type = 'driver'
        elif 'iron' in club_name.lower():
            club_type = 'iron'
        elif 'wedge' in club_name.lower():
            club_type = 'wedge'
        elif 'putter' in club_name.lower():
            club_type = 'putter'
        elif 'ybrid' in club_name.lower() or 'rescue' in club_name.lower() or 'utility' in club_name.lower() or 'UDI' in club_name.lower():
            club_type = 'hybrid/rescue/utility'
        elif 'fairway' in club_name.lower() or 'wood' in club_name.lower():
            club_type = 'fairway wood'
        elif 'complete set' in club_name.lower():
            club_type = 'set'
        else:
            club_type = 'NA'
        
        yield {
            'name': club_name,
            'type': club_type,
            'price': price,
            'link': link,
            'condition': condition
        }
