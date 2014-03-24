from django.db import models
from decimal import Decimal


class Invoice(models.Model):
	invoice_number = models.TextField()
	invoiced_customer_name = models.TextField()
	invoiced_customer_address = models.TextField()
	vendors_name = models.TextField()
	vendors_address = models.TextField()
	net_amount = models.TextField()
	tax_type = models.TextField()
	tax_rate = models.TextField(default='0')
	tax_amount = models.TextField()
	total_payable = models.TextField()

	def save(self, *args, **kwargs):
		self.full_clean(exclude=['net_amount', 'tax_amount', 'total_payable'])
		super().save(*args, **kwargs)


class Line_item(models.Model):
	line_item = models.TextField()
	line_item_description = models.TextField()
	line_item_price = models.TextField()
	line_item_quantity = models.TextField()
	invoice = models.ForeignKey(Invoice)
	line_item_total = models.TextField()

	def save(self, *args, **kwargs):
		if self.line_item is False or self.line_item == '':
			return
		if self.line_item_price is False or self.line_item_price == '':
			return
		if self.line_item_quantity is False or self.line_item_quantity == '':
			return
		self.line_item_total = "{:.2f}".format(float(self.line_item_price) * float(self.line_item_quantity))
		super().save(*args, **kwargs)
		self.update_totals()
	
	def update_totals(self):
		invoice_ = self.invoice
		net_amount, tax_amount, total_payable = (0, 0, 0)
		for item in Line_item.objects.filter(invoice=invoice_):
			net_amount += float(item.line_item_total)
		tax_rate = float(invoice_.tax_rate)/100
		invoice_.tax_amount = "{:.2f}".format(tax_rate * net_amount)
		invoice_.total_payable = "{:.2f}".format(net_amount + (net_amount * tax_rate))
		invoice_.net_amount = "{:.2f}".format(net_amount)
		invoice_.save()

class Currency(models.Model):
	currency_symbol = models.TextField()
	currency_name = models.TextField()
	invoice = models.ForeignKey(Invoice)

