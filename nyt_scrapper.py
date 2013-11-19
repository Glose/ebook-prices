import bs4
import json
import requests


def scrap(url):
	soup = bs4.BeautifulSoup(requests.get(url).text)
	table = soup.find(class_='bestSellersList')
	res = []
	for book in soup.find_all(class_='bookDetails'):
		title = book.find(class_='bookName').text[:-2]
		summary = book.find(class_='summary').text
		author = summary.split('by', 1)[1].split('(', 1)[0][1:-2]
		res.append({'title': title, 'author': author})
	return res

def best_sellers():
	res = []
	res += scrap('http://www.nytimes.com/best-sellers-books/2013-11-24/combined-print-and-e-book-nonfiction/list.html')
	res += scrap('http://www.nytimes.com/best-sellers-books/2013-11-24/combined-print-and-e-book-fiction/list.html')
	return res


if __name__ == '__main__':
	print(best_sellers())