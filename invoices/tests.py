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


class ListViewTest(TestCase):

	def test_display_all_line_items(self):
		Line_item.objects.create(
			line_item='Line Item 1',
			line_item_description='Description 1',
			line_item_quantity='1'
		)

		Line_item.objects.create(
			line_item='Line Item 2',
			line_item_description='Description 2',
			line_item_quantity='2'
		)

		response = self.client.get('/invoices/the-only-invoice-in-the-world/')
		
		self.assertContains(response, 'Line Item 1')
		self.assertContains(response, 'Line Item 2')


class LineItemModelTest(TestCase):

	def test_uses_invoice_template(self):
		response = self.client.get('/invoices/the-only-invoice-in-the-world/')
		self.assertTemplateUsed(response, 'invoice.html')

	def test_saving_and_retrieving_line_items(self):
		first_line_item = Line_item()
		first_line_item.line_item = 'Item #1'
		first_line_item.line_item_description = 'Description of Item #1'
		first_line_item.line_item_quantity = '2'
		first_line_item.save()

		second_line_item = Line_item()
		second_line_item.line_item = 'Item #2'
		second_line_item.line_item_description = 'Description of Item #2'
		second_line_item.line_item_quantity = '1'
		second_line_item.save()

		saved_line_items = Line_item.objects.all()
		self.assertEqual(saved_line_items.count(), 2)

		first_saved_line_item = saved_line_items[0]
		second_saved_line_item = saved_line_items[1]
		self.assertEqual(first_saved_line_item.line_item, first_line_item.line_item)
		self.assertEqual(second_saved_line_item.line_item_quantity, second_line_item.line_item_quantity)


class NewInvoiceTest(TestCase):

	def test_saving_a_POST_request(self):
		self.client.post(
			'/invoices/new',
			data={
				'line_item': 'Item #1',
				'line_item_description': 'Description of Item #1',
				'line_item_quantity': '2'
			}
		)
		self.assertEqual(Line_item.objects.count(), 1)
		new_line_item = Line_item.objects.first()
		self.assertEqual(new_line_item.line_item, 'Item #1')

	def test_redirects_after_POST(self):
		response = self.client.post(
			'/invoices/new',
			data={
				'line_item': 'Item #1',
				'line_item_description': 'Description of Item #1',
				'line_item_quantity': '2'
			}
		)
		self.assertRedirects(response, '/invoices/the-only-invoice-in-the-world/')

