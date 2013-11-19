#!/usr/bin/env python2

import amazon
import nyt_scrapper
import json


books = nyt_scrapper.best_sellers()
books = amazon.prices(books)

res = json.dumps(books, indent=4, separators=(', ', ': '))

with open('results.json', 'w') as f:
	f.write(res)
print(res)