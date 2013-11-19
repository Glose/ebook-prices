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
		book['price'] = 0
	return books
