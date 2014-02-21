from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from invoices.views import home_page
from invoices.models import Invoice, Line_item

class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)

	def test_home_page_can_save_a_POST_request(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['invoice_number'] = '1234'

		response = home_page(request)

		self.assertIn('1234', response.content.decode())
		expected_html = render_to_string(
			'home.html',
			{'invoice_number_output': '1234'}
		)
		self.assertEqual(response.content.decode(), expected_html)

	def test_saving_and_retrieving_invoices(self):
		first_invoice = Invoice()
		first_invoice.invoice_number = '1234'
		first_invoice.invoiced_customer_name = 'Bob Buyer'
		first_invoice.save()

		second_invoice = Invoice()
		second_invoice.invoice_number = '4321'
		second_invoice.vendors_name = 'Sally Seller'
		second_invoice.save()

		saved_invoices = Invoice.objects.all()
		self.assertEqual(saved_invoices.count(), 2)

		first_saved_invoice = saved_invoices[0]
		second_saved_invoice = saved_invoices[1]
		self.assertEqual(first_saved_invoice.invoice_number, first_invoice.invoice_number)
		self.assertEqual(second_saved_invoice.invoice_number, second_invoice.invoice_number)

