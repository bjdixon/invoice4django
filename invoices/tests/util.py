from invoices.views import home_page
from invoices.models import Invoice, Line_item, Currency

def create_new_invoice(alt=0):
	if alt == 1:
		return Invoice.objects.create(
			invoice_number='1234',
			invoiced_customer_name='C Name',
			invoiced_customer_address='123 another customer address',
			vendors_name='V Name',
			vendors_address='123 another vendors address',
			tax_type='CST',
			tax_rate='20'
		)
	return Invoice.objects.create(
		invoice_number='1234',
		invoiced_customer_name='C Name',
		invoiced_customer_address='123 customer address',
		vendors_name='V Name',
		vendors_address='123 vendors address',
		tax_type='TST',
		tax_rate='15'
	)

def create_new_line_item(invoice_, num='1'):	
	return Line_item.objects.create(
		line_item='Line Item %s' % (num,),
		line_item_description='Description %s' % (num,),
		line_item_quantity='%s' % (num,),
		line_item_price='%s00' % (num,),
		invoice=invoice_
	)

def create_POST_data():
	return {
		'invoice_number': '1234',
		'invoiced_customer_name': 'C Name',
		'invoiced_customer_address': '123 address',
		'vendors_name': 'V Name',
		'vendors_address': '123 address',
		'tax_type': 'TST',
		'tax_rate': '15',
		'currency_symbol': '$',
		'currency_name': 'CAD',
		'line_item': 'Item #1',
		'line_item_description': 'Description of Item #1',
		'line_item_quantity': '2',
		'line_item_price': '100'
	}

