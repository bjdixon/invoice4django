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
		self.assertEqual(response.content.decode(), expected_html)
	
	def test_home_page_renders_home_template(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')


class VendorPageTest(TestCase):

	def test_add_vendor_page_returns_correct_html(self):
		invoice_ = create_new_invoice()
		request = HttpRequest()
		response = vendor_page(request, invoice=invoice_)
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
		response = customer_page(request, invoice=invoice_)
		expected_html = render_to_string('customer.html', {'form': CustomerForm()})
		self.assertMultiLineEqual(response.content.decode(), expected_html)

	def test_add_customer_page_renders_customer_template(self):
		invoice_ = create_new_invoice()
		response = self.client.get('/invoices/%d/customer/' % (invoice_.id))
		self.assertTemplateUsed(response, 'customer.html')


class LineItemPageTest(TestCase):

	def test_line_item_page_returns_correct_html(self):
		invoice_ = create_new_invoice()
		request = HttpRequest()
		response = line_item_page(request, invoice=invoice_)
		expected_html = render_to_string('line_item.html', {'form': LineItemForm()})
		self.assertMultiLineEqual(response.content.decode(), expected_html)

	def test_line_item_page_renders_line_item_template(self):
		invoice_ = create_new_invoice()
		response = self.client.get('/invoices/%d/line_item/' % (invoice_.id))
		self.assertTemplateUsed(response, 'line_item.html')

	def test_correct_invoice_is_being_passed_to_template(self):
		pass

	def test_displays_correct_details_for_that_invoice(self):
		pass

	def test_only_line_items_for_this_invoice_are_displayed(self):
		pass


class NewInvoiceTest(TestCase):

	def test_saving_a_POST_request(self):
		pass

	def test_redirects_after_POST(self):
		pass

	def test_POST_request_saves_invoice_currency_and_tax_data(self):
		pass

	def test_validation_errors_sent_back_to_home_page_template(self):
		pass


class NewVendorTest(TestCase):

	def test_saving_a_POST_request(self):
		pass

	def test_redirects_after_POST(self):
		pass

	def test_POST_request_saves_vendor_and_associates_correct_invoice(self):
		pass

	def test_validation_errors_sent_back_to_vendor_template(self):
		pass


class NewCustomerTest(TestCase):

	def test_saving_a_POST_request(self):
		pass

	def test_redirects_after_POST(self):
		pass

	def test_POST_request_saves_customer_and_associates_correct_invoice(self):
		pass

	def test_validation_errors_sent_back_to_customer_template(self):
		pass


class NewLineItemTest(TestCase):

	def test_saving_a_POST_request(self):
		pass

	def test_redirects_after_POST(self):
		pass

	def test_POST_request_saves_line_item_and_associates_correct_invoice(self):
		pass

	def test_validation_errors_sent_back_to_line_item_template(self):
		pass


