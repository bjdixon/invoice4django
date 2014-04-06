from django.core.urlresolvers import resolve
from django.test import TestCase
from unittest import skip
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape
from .utils import *

from invoices.views import *
from invoices.models import *
from invoices.forms import *


class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)
	
	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html', {
			'invoice_form': InvoiceForm(),
			'currency_form': CurrencyForm(),
			'tax_form': TaxForm(),
		})
		self.assertIn(response.content.decode(), expected_html)
	
	def test_home_page_renders_home_template(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response.content.decode(), 'home.html')


class VendorPageTest(TestCase):

	def test_add_vendor_page_returns_correct_html(self):
		self.maxDiff = None
		invoice_ = create_new_invoice()
		request = HttpRequest()
		response = vendor_page(request, invoice=invoice_.id)
		expected_html = render_to_string('vendor.html', {'form': VendorForm()})
		self.assertMultiLineEqual(response.content.decode(), expected_html)

	def test_add_vendor_page_renders_vendor_template(self):
		invoice_ = create_new_invoice()
		response = self.client.get('/invoices/%d/vendor/' % (invoice_.id))
		self.assertTemplateUsed(response, 'vendor.html')


class CustomerPageTest(TestCase):

	def test_add_customer_page_returns_correct_html(self):
		invoice_ = create_new_invoice()
		request = HttpRequest()
		response = customer_page(request, invoice=invoice_.id)
		expected_html = render_to_string('customer.html', {'form': CustomerForm()})
		self.assertMultiLineEqual(response.content.decode(), expected_html)

	def test_add_customer_page_renders_customer_template(self):
		invoice_ = create_new_invoice()
		response = self.client.get('/invoices/%d/customer/' % (invoice_.id))
		self.assertTemplateUsed(response, 'customer.html')


class LineItemPageTest(TestCase):

	def test_line_item_page_returns_correct_html(self):
		self.maxDiff = None
		invoice_ = create_new_invoice()
		create_related_invoice_models(invoice=invoice_)
		request = HttpRequest()
		response = line_item_page(request, invoice=invoice_.id)
		self.assertIn('Invoice number: 4321', response.content.decode())
		self.assertIn('Please pay one day', response.content.decode())
		self.assertIn('USD(15%)', response.content.decode())

	def test_line_item_page_renders_line_item_template(self):
		invoice_ = create_new_invoice()
		create_related_invoice_models(invoice_)
		response = self.client.get('/invoices/%d/line_item/' % (invoice_.id))
		self.assertTemplateUsed(response, 'line_item.html')

	def test_correct_invoice_is_being_passed_to_template(self):
		invoice_ = create_new_invoice()
		create_related_invoice_models(invoice_)
		response = self.client.get('/invoices/%d/line_item/' % (invoice_.id))
		self.assertTemplateUsed(response, 'line_item.html')


	def test_displays_correct_details_for_that_invoice(self):
		self.maxDiff = None
		invoice_ = create_new_invoice()
		create_related_invoice_models(invoice_)
		response = self.client.get('/invoices/%d/line_item/' % (invoice_.id))
		self.assertIn('Please pay one day', response.content.decode())

	def test_only_line_items_for_this_invoice_are_displayed(self):
		self.maxDiff = None
		invoice_ = create_new_invoice()
		create_related_invoice_models(invoice_)	
		alt_invoice = create_new_invoice()
		line_item_ = create_new_line_item(invoice=invoice_)
		alt_line_item = create_new_line_item(invoice=alt_invoice, num=2)
		response = self.client.get('/invoices/%d/line_item/' % (invoice_.id))
		self.assertIn('Line Item 1', response.content.decode())


class NewInvoiceTest(TestCase):

	def test_saving_a_POST_request(self):
		self.client.post(
			'/invoices/', 
			data={
				'invoice_number': '1234',
				'invoice_comment': 'comment',
				'invoice_date': '04/05/2014',
				'currency_name': 'USD',
				'currency_symbol': '$',
				'tax_name': 'HST',
				'tax_rate': '10',
			}
		)
		self.assertEqual(Invoice.objects.count(), 1)
		self.assertEqual(Currency.objects.count(), 1)
		self.assertEqual(Tax.objects.count(), 1)
		new_invoice = Invoice.objects.first()
		new_currency = Currency.objects.first()
		new_tax = Tax.objects.first()
		self.assertEqual(new_invoice.invoice_number, '1234')
		self.assertEqual(new_currency.currency_symbol, '$')
		self.assertEqual(new_tax.tax_rate, 10)

	def test_redirects_after_POST(self):
		response = self.client.post(
			'/invoices/',
			data={
				'invoice_number': '1234',
				'invoice_date': '04/05/2014',
				'invoice_comment': 'comment',
				'currency_name': 'USD',
				'currency_symbol': '$',
				'tax_name': 'TST',
				'tax_rate': '10',
			}
		)
		invoice = Invoice.objects.first()
		self.assertRedirects(response, '/invoices/%d/vendor/' % (invoice.id,))

	@skip
	def test_validation_errors_sent_back_to_home_page_template(self):
		response = self.client.post(
			'/invoices/',
			data={
				'invoice_number': '',
				'invoice_date': '',
				'invoice_comment': '',
			}
		)
		self.assertEqual(Invoice.objects.count(), 0)
		self.assertTemplateUsed(response, 'home.html')
		self.assertIn('This field is required', response.content.decode())


class NewVendorTest(TestCase):

	def test_saving_a_POST_request(self):
		invoice = create_new_invoice()
		self.client.post(
			'/invoices/%d/vendor/' % (invoice.id,), 
			data={
				'vendor_name': 'vname',
				'vendor_street_address': 'vaddress',
				'vendor_city': 'city',
				'vendor_state': 'US',
				'vendor_post_code': 'code',
				'vendor_phone_number': '123 123 1234',
				'vendor_email_address': 'vendor@email.com',
			}
		)
		self.assertEqual(Vendor.objects.count(), 1)
		vendor = Vendor.objects.first()
		self.assertEqual(vendor.vendor_name, 'vname')
		self.assertEqual(vendor.vendor_email_address, 'vendor@email.com')
		self.assertEqual(vendor.vendor_state, 'US')

	def test_redirects_after_POST(self):
		invoice = create_new_invoice()
		response = self.client.post(
			'/invoices/%d/vendor/' % (invoice.id,),
			data={
				'vendor_name': 'vname',
				'vendor_street_address': 'vaddress',
				'vendor_city': 'city',
				'vendor_state': 'US',
				'vendor_post_code': 'code',
				'vendor_phone_number': '123 123 1234',
				'vendor_email_address': 'vendor@email.com',
			}
		)
		invoice = Invoice.objects.first()
		self.assertRedirects(response, '/invoices/%d/customer/' % (invoice.id,))

	def test_validation_errors_sent_back_to_vendor_template(self):
		pass


class NewCustomerTest(TestCase):

	def test_saving_a_POST_request(self):
		invoice = create_new_invoice()
		self.client.post(
			'/invoices/%d/customer/' % (invoice.id,), 
			data={
				'customer_name': 'cname',
				'customer_street_address': 'caddress',
				'customer_city': 'city',
				'customer_state': 'US',
				'customer_post_code': 'code',
				'customer_phone_number': '123 123 1234',
				'customer_email_address': 'customer@email.com',
			}
		)
		self.assertEqual(Customer.objects.count(), 1)
		customer = Customer.objects.first()
		self.assertEqual(customer.customer_name, 'cname')
		self.assertEqual(customer.customer_email_address, 'customer@email.com')
		self.assertEqual(customer.customer_state, 'US')

	def test_redirects_after_POST(self):
		invoice = create_new_invoice()
		vendor = create_new_vendor()
		vendor.invoice = invoice
		vendor.save()
		create_new_currency(invoice=invoice)
		create_new_tax(invoice=invoice)
		response = self.client.post(
			'/invoices/%d/customer/' % (invoice.id,),
			data={
				'customer_name': 'cname',
				'customer_street_address': 'caddress',
				'customer_city': 'city',
				'customer_state': 'US',
				'customer_post_code': 'code',
				'customer_phone_number': '123 123 1234',
				'customer_email_address': 'customer@email.com',
			}
		)
		invoice = Invoice.objects.first()
		self.assertRedirects(response, '/invoices/%d/line_item/' % (invoice.id,))

	def test_validation_errors_sent_back_to_customer_template(self):
		pass


class NewLineItemTest(TestCase):

	def test_saving_a_POST_request(self):
		invoice = create_new_invoice()
		self.client.post(
			'/invoices/%d/line_item/' % (invoice.id,),
			data={
				'line_item': 'Line item 1',
				'line_item_description': 'Description 1',
				'line_item_quantity': '1',
				'line_item_price': '100',
			}
		)
		self.assertEqual(Line_item.objects.count(), 1)
		new_line_item = Line_item.objects.first()
		self.assertEqual(new_line_item.line_item_description, 'Description 1')

	def test_redirects_after_POST(self):
		invoice = create_new_invoice()
		create_related_invoice_models(invoice=invoice)
		response = self.client.post(
			'/invoices/%d/line_item/' % (invoice.id,),
			data={
				'line_item': 'Line item 1',
				'line_item_description': 'Description 1',
				'line_item_quantity': '1',
				'line_item_price': '100',
			}
		)
		invoice = Invoice.objects.first()
		self.assertRedirects(response, '/invoices/%d/line_item/' % (invoice.id,))

	def test_validation_errors_sent_back_to_line_item_template(self):
		pass


