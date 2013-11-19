"""
You need a ~/.amazon-product-api file with this content:

[Credentials]
access_key = <your access key>
secret_key = <your secret key>
associate_tag = <your associate id>
"""

from amazonproduct import API


api = API(locale='us')

def prices(books):
	for book in books:
		author = book['author'].split(' with ')[0]
		for item in api.item_search('KindleStore', Author=author, Title=book['title'], ResponseGroup='OfferSummary'):
			try:
				book['amazon-price'] = int(item.ItemAttributes.ListPrice.Amount.text)
			except AttributeError:
				print('No amazon price found for ' + book['title'])
				book['amazon-price'] = None
			break
	return books
