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

class Line_item(models.Model):
	line_item = models.TextField()
	line_item_description = models.TextField()
	line_item_price = models.TextField()
	line_item_quantity = models.TextField()
	invoice = models.ForeignKey(Invoice)
	line_item_total = models.TextField()

	def save(self, *args, **kwargs):
		self.full_clean(exclude=['line_item_total'])
		self.update_totals()
		super().save(*args, **kwargs)

	def update_totals(self):
		self.line_item_total = "{:.2f}".format(float(self.line_item_price) * float(self.line_item_quantity))
		invoice_ = self.invoice
		tax_amount = float(self.line_item_total) * float(invoice_.tax_rate)/100
		total_payable = float(self.line_item_total) + tax_amount
		for item in Line_item.objects.filter(invoice=invoice_):
			if item.id != self.id:
				tax_amount += float(item.line_item_total) + float(item.line_item_total) * float(invoice_.tax_rate)/100
				total_payable += tax_amount + float(item.line_item_total) 

		invoice_.tax_amount = "{:.2f}".format(tax_amount)
		invoice_.total_payable = "{:.2f}".format(total_payable)
		invoice_.net_amount = "{:.2f}".format(total_payable - tax_amount)
		invoice_.save()


class Currency(models.Model):
	currency_symbol = models.TextField()
	currency_name = models.TextField()
	invoice = models.ForeignKey(Invoice)

