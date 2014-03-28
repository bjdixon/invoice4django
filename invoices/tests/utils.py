import time
import datetime
from invoices.models import Invoice, Line_item, Currency, Vendor, Customer, Tax

def create_new_invoice(alt=0):
	if alt == 1:
		return Invoice.objects.create(
			invoice_number='1234',
			invoice_date=datetime.date.today(),
			invoice_comment='Please pay promptly'
		)
	return Invoice.objects.create(
		invoice_number='4321',
		invoice_date=datetime.date.today(),
		invoice_comment='Please pay one day'
	)

def create_new_currency(invoice):
	return Currency.objects.create(
		currency_symbol='$',
		currency_name='USD',
		invoice=invoice
	)
	
def create_new_tax(invoice):
	return Tax.objects.create(
		tax_rate=15,
		tax_name='USD',
		invoice=invoice
	)
	
def create_new_vendor():
	return Vendor.objects.create(
		vendor_name='Vendor Name',
		vendor_street_address='123 vendor street',
		vendor_city='Vendor City',
		vendor_state='VS',
		vendor_post_code='Vendor code',
		vendor_phone_number='123 123 1234',
		vendor_email_address='vendor@email.com'
	)
	
def create_new_customer():
	return Customer.objects.create(
		customer_name='Customer Name',
		customer_street_address='123 customer street',
		customer_city='Customer City',
		customer_state='CS',
		customer_post_code='Customer code',
		customer_phone_number='123 123 1234',
		customer_email_address='customer@email.com'
	)
	
def create_new_line_item(invoice, num=1):	
	return Line_item.objects.create(
		line_item='Line Item %s' % (num,),
		line_item_description='Description %s' % (num,),
		line_item_quantity=num,
		line_item_price=num*100,
		invoice=invoice
	)

