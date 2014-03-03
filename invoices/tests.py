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


class InvoiceViewTest(TestCase):

	def test_uses_invoice_template(self):
		invoice_ = Invoice.objects.create()
		response = self.client.get('/invoices/%d/' % (invoice_.id,))
		self.assertTemplateUsed(response, 'invoice.html')

	def test_display_only_items_for_that_list(self):
		correct_invoice = Invoice.objects.create()
		Line_item.objects.create(
			line_item='Line Item 1',
			line_item_description='Description 1',
			line_item_quantity='1',
			invoice=correct_invoice
		)
		Line_item.objects.create(
			line_item='Line Item 2',
			line_item_description='Description 2',
			line_item_quantity='2',
			invoice=correct_invoice
		)
		other_invoice = Invoice.objects.create()

		Line_item.objects.create(
			line_item='Other Line Item 1',
			line_item_description='Description 1',
			line_item_quantity='1',
			invoice=other_invoice
		)
		Line_item.objects.create(
			line_item='Other Line Item 2',
			line_item_description='Description 2',
			line_item_quantity='2',
			invoice=other_invoice
		)

		response = self.client.get('/invoices/%d/' % (correct_invoice.id,))
		
		self.assertContains(response, 'Line Item 1')
		self.assertContains(response, 'Line Item 2')

		self.assertNotContains(response, 'Other Line Item 1')
		self.assertNotContains(response, 'Other Line Item 2')

	def test_passes_correct_invoice_to_template(self):
		other_invoice = Invoice.objects.create()
		correct_invoice = Invoice.objects.create()
		response = self.client.get('/invoices/%d/' % (correct_invoice.id,))
		self.assertEqual(response.context['invoice'], correct_invoice)


class InvoiceAndLineItemModelTest(TestCase):

	def test_saving_and_retrieving_line_items(self):
		invoice_ = Invoice()
		invoice_.save()
		first_line_item = Line_item()
		first_line_item.line_item = 'Item #1'
		first_line_item.line_item_description = 'Description of Item #1'
		first_line_item.line_item_quantity = '2'
		first_line_item.invoice = invoice_
		first_line_item.save()

		second_line_item = Line_item()
		second_line_item.line_item = 'Item #2'
		second_line_item.line_item_description = 'Description of Item #2'
		second_line_item.line_item_quantity = '1'
		second_line_item.invoice = invoice_
		second_line_item.save()

		saved_invoice = Invoice.objects.first()
		self.assertEqual(saved_invoice, invoice_)

		saved_line_items = Line_item.objects.all()
		self.assertEqual(saved_line_items.count(), 2)

		first_saved_line_item = saved_line_items[0]
		second_saved_line_item = saved_line_items[1]
		self.assertEqual(first_saved_line_item.line_item, 'Item #1')
		self.assertEqual(first_saved_line_item.invoice, invoice_)
		self.assertEqual(second_saved_line_item.line_item, 'Item #2')
		self.assertEqual(second_saved_line_item.invoice, invoice_)


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
		new_invoice = Invoice.objects.first()
		self.assertRedirects(response, '/invoices/%d/' % (new_invoice.id,))


class NewItemTest(TestCase):

	def test_can_save_a_POST_request_to_an_existing_invoice(self):
		other_invoice = Invoice.objects.create()
		correct_invoice = Invoice.objects.create()

		self.client.post(
			'/invoices/%d/new_item' % (correct_invoice.id,),
			data={
				'line_item': 'Item #1',
				'line_item_description': 'Description of Item #1',
				'line_item_quantity': '2'
			}
		)

		self.assertEqual(Line_item.objects.count(), 1)
		new_item = Line_item.objects.first()
		self.assertEqual(new_item.line_item, 'Item #1')
		self.assertEqual(new_item.invoice, correct_invoice)

	def test_redirects_to_invoice_view(self):
		other_invoice = Invoice.objects.create()
		correct_invoice = Invoice.objects.create()

		response = self.client.post(
			'/invoices/%d/new_item' % (correct_invoice.id,),
			data={
				'line_item': 'Item #1',
				'line_item_description': 'Description of Item #1',
				'line_item_quantity': '2'
			}
		)
		self.assertRedirects(response, '/invoices/%d/' % (correct_invoice.id,))


