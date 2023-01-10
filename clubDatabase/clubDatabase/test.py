import json

with open('titleistLinks.json', 'r') as f:
    data = json.load(f)

links = [item['link'] for item in data]

print(links)