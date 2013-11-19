import itunes

books = itunes.search(query='eragon', media='ebook')
for book in books:
	print book.get_name(), book.get_price()
