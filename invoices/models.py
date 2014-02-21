from django.db import models

class Invoice(models.Model):
	invoice_number = models.TextField()
	invoiced_customer_name = models.TextField()
	invoiced_customer_address = models.TextField()
	vendors_name = models.TextField()
	vendors_address = models.TextField()
	tax_type = models.TextField()
	tax_rate = models.TextField()

class Line_item(object):
	line_item = models.TextField()
	line_item_description = models.TextField()
	line_item_price = models.TextField()
	line_item_quantity = models.TextField()

