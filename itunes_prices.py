import itunes


def prices(books):
	for book in books:
		for item in itunes.search(query=book['title'], media='ebook'):
			book['itunes-price'] = item.price * 100
			break
	return books