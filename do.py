#!/usr/bin/env python2

import amazonproduct
import bs4
import itunes as itunes_
import json
import re
import requests

api = amazonproduct.API(locale='us')

def scrap(url):
	soup = bs4.BeautifulSoup(requests.get(url).text)
	table = soup.find(class_='bestSellersList')
	res = []
	for book in soup.find_all(class_='bookDetails'):
		title = book.find(class_='bookName').text[:-2]
		summary = book.find(class_='summary').text
		author = summary.split('by', 1)[1].split('(', 1)[0][1:-2].split(' and ')[0].split(' with ')[0]
		res.append({'title': title, 'author': author})
	return res

def itunes(book):
	item = itunes_.search(query=book['title'] + ' ' + book['author'], media='ebook')[0]
	book['itunes_id'] = item.id
	book['itunes'] = item.price

def amazon(book):
	item = next(iter(api.item_search('KindleStore', Author=book['author'], Title=book['title'])))
	book['asin'] = item.ASIN.text
	soup = bs4.BeautifulSoup(requests.get(
		'http://www.amazon.com/dp/{}'.format(book['asin']),
		headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36'},
	).text)
	try:
		price = soup.find(id=re.compile(r'^tmm_')).find(class_='price').text.strip()
	except AttributeError:
		book['amazon'] = None
	else:
		book['amazon'] = None if price == '--' else float(price[1:])



books = []
books += scrap('http://www.nytimes.com/best-sellers-books/2013-11-24/combined-print-and-e-book-nonfiction/list.html')
books += scrap('http://www.nytimes.com/best-sellers-books/2013-11-24/combined-print-and-e-book-fiction/list.html')

for book in books:
	itunes(book)
	amazon(book)

	book['title'] = book['title'].lower().capitalize()

	if book['amazon']:
		book['amazon_'] = '${}'.format(book['amazon'])
		book['variation'] = '{:.3}'.format(100 * (book['itunes'] - book['amazon']) / book['amazon'])
	else:
		book['variation'] = 'NA'
		book['amazon_'] = 'NA'


with open('README.md', 'w') as f:
	f.write("""ebook-prices
============

Compare Ebook prices from Kindle and iBooks


| Book | Kindle price | iBooks price | Variation (% from Kindle to iBooks) |
| ---- | ------------:| ------------:| ----:|
""")
	for book in books:
		f.write('| {title} | <a href="http://www.amazon.com/dp/{asin}">{amazon_}</a> | <a href="https://itunes.apple.com/us/book/id{itunes_id}">${itunes}</a> | {variation:.3} |\n'.format(**book))

with open('results.json', 'w') as f:
	json.dump(books, f, indent=4, separators=(',', ': '))
