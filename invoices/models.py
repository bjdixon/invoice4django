from decimal import *
from django.db import models
from decimal import Decimal


class Invoice(models.Model):
	invoice_number = models.CharField(max_length=32)
	invoice_date = models.DateField()
	invoice_comment = models.TextField()

	def get_net_total(self):
		line_items = Line_item.objects.select_related().filter(invoice=self)
		return sum([
			item.line_item_price * item.line_item_quantity for item in line_items
		])

	def get_tax_total(self):
		taxes = Tax.objects.filter(invoice=self)
		final_tax_rate = sum([
			tax.tax_rate for tax in taxes
		])
		return self.get_net_total() * final_tax_rate / 100	

	def get_total_payable(self):
		return self.get_net_total() + self.get_tax_total()	

	def delete(self, *args, **kwargs):
		Line_item.objects.filter(invoice=self).delete()
		Tax.objects.filter(invoice=self).delete()
		Currency.objects.filter(invoice=self).delete()
		Customer.objects.filter(invoice=self).delete()
		super().delete(*args, **kwargs)

class Line_item(models.Model):
	line_item = models.CharField(max_length=128)
	line_item_description = models.TextField()
	line_item_price = models.DecimalField(max_digits=16, decimal_places=2)
	line_item_quantity = models.IntegerField()
	invoice = models.ForeignKey(Invoice)

	def get_line_item_total(self):
		return self.line_item_price * self.line_item_quantity
	

class Currency(models.Model):
	currency_symbol = models.CharField(max_length=8)
	currency_name = models.CharField(max_length=32)
	invoice = models.ForeignKey(Invoice)


class Vendor(models.Model):
	vendor_name = models.CharField(max_length=32)
	vendor_street_address = models.CharField(max_length=80)
	vendor_city = models.CharField(max_length=32)
	vendor_state = models.CharField(max_length=32)
	vendor_post_code = models.CharField(max_length=16)
	vendor_phone_number = models.CharField(max_length=24)
	vendor_email_address = models.EmailField(max_length=128)
	invoice = models.ForeignKey(Invoice, blank=True, null=True)


class Customer(models.Model):
	customer_name = models.CharField(max_length=32)
	customer_street_address = models.CharField(max_length=80)
	customer_city = models.CharField(max_length=32)
	customer_state = models.CharField(max_length=32)
	customer_post_code = models.CharField(max_length=16)
	customer_phone_number = models.CharField(max_length=24)
	customer_email_address = models.EmailField(max_length=128)
	invoice = models.ForeignKey(Invoice, blank=True, null=True)


class Tax(models.Model):
	tax_name = models.CharField(max_length=32)
	tax_rate = models.DecimalField(max_digits=5, decimal_places=2)
	invoice = models.ForeignKey(Invoice)


