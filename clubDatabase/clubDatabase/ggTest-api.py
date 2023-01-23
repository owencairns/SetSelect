import requests
import json

url = 'https://prod-catalog-product-api.dickssportinggoods.com/v2/search?searchVO=%7B%22selectedCategory%22%3A%2210051_76724%22%2C%22selectedStore%22%3A%22420%22%2C%22selectedSort%22%3A5%2C%22selectedFilters%22%3A%7B%7D%2C%22storeId%22%3A10701%2C%22pageNumber%22%3A{}%2C%22pageSize%22%3A144%2C%22totalCount%22%3A1327%2C%22searchTypes%22%3A%5B%22PINNING%22%5D%2C%22isFamilyPage%22%3Atrue%2C%22snbAudience%22%3A%22%22%7D'
response = requests.get(url.format(0))
data = response.json()
pages = int(int(data['totalCount']) / 144)

product_data = []
for i in range(0, pages+1):
    response = requests.get(url.format(i))
    data = response.json()
    products = data['productVOs']
    for product in products:
        attr = product['attributes']
        attr_list = json.loads(attr)
        cat = [d["5382"] for d in attr_list if "5382" in d]
        for all in product['floatFacets']:
            if all['identifier'] == 'golfgalaxyofferprice':      
                product_data.append({
                    'name': product['name'],
                    'price': all['value'],
                    'manufacturer': product['mfName'],
                    'link': 'https://www.golfgalaxy.com/' + product['assetSeoUrl'],
                    'category': cat[0]
                })

with open('ggClubs.json', "w") as f:
    f.write('[\n')
    for i, datum in enumerate(product_data):
        f.write(json.dumps(datum))
        if i != len(product_data)-1:
            f.write(",\n")
        else:f.write('\n')
    f.write(']')