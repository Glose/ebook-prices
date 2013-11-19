#!/usr/bin/env python2

import amazon
import itunes_prices
import nyt_scrapper
import json


books = nyt_scrapper.best_sellers()
books = amazon.prices(books)
books = itunes_prices.prices(books)

res = json.dumps(books, indent=4, separators=(', ', ': '))

with open('results.json', 'w') as f:
	f.write(res)

formatted = []
for book in res:
    a = book['amazon-price']/100
    i = book['itunes-price']/100
    formatted.append({
    	'title': book['title'].lower(),
    	'amazon': a,
    	'itunes': i,
    	'variation': 100*(i-a)/a,
    })

print('| {} | ${} | ${} | {:.3} |'.format(b['title'].lower().capitalize(), a, i, 100*(a-i)/a))
with open('README.md', 'w') as f:
	f.write("""ebook-prices
============

Compare Ebook prices from Kindle and iBooks


| Book | Amazon price | iBooks price | Variation (% from Amazon to iBooks) |
| ---- | ------------:| ------------:| ----:|
""")
	for book in formatted:
		f.write('| {title} | ${amazon} | ${itunes} | {variation:.3} |\n'.format(**book)

print(res)