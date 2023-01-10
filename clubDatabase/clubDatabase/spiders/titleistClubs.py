# import scrapy
# from scrapy.exporters import JsonItemExporter
# import json

# with open('titleistLinks.json', 'r') as f:
#     data = json.load(f)

# links = [item['link'] for item in data]

# class TitleistClubs(scrapy.Spider):
#     name = 'titleistClubs'
#     start_urls = links
#     def parse(self, response):

#         # Extract the data
#         club_name = response.css('h1.product-name::text').get()
#         price = response.css('span.price-sales::text').get()
#         url = response.request.url

#         stripped_shaft_options = []
#         for option in response.css('div.select-container'):
#             current = option.css('span.label::text').get()
#             current = current.strip()
#             if current == 'clubs.label.shaftid':
#                 shaft_options = option.css('option::text').getall()
#                 stripped_shaft_options = [s.strip() for s in shaft_options]

#         yield {
#             'name': club_name.strip(),
#             'price': price.strip(),
#             'url': url,
#             'shaft options': stripped_shaft_options
#         }