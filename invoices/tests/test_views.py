from django.core.urlresolvers import resolve
from django.test import TestCase
from unittest import skip
from django.http import HttpRequest
from django.template.loader import render_to_string

from invoices.views import home_page
from invoices.models import Invoice, Line_item, Currency
from .util import create_new_invoice

class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)

	def test_home_page_renders_home_template(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')


class InvoiceViewTest(TestCase):

	def test_uses_invoice_template(self):
		invoice_ = Invoice.objects.create()
		response = self.client.get('/invoices/%d/' % (invoice_.id,))
		self.assertTemplateUsed(response, 'invoice.html')

	def test_display_only_items_for_that_invoice(self):
		correct_invoice = Invoice.objects.create()
		Line_item.objects.create(
			line_item='Line Item 1',
			line_item_description='Description 1',
			line_item_quantity='1',
			line_item_price='100',
			invoice=correct_invoice
		)
		Line_item.objects.create(
			line_item='Line Item 2',
			line_item_description='Description 2',
			line_item_quantity='2',
			line_item_price='10',
			invoice=correct_invoice
		)
		other_invoice = Invoice.objects.create()

		Line_item.objects.create(
			line_item='Other Line Item 1',
			line_item_description='Description 1',
			line_item_quantity='1',
			line_item_price='100',
			invoice=other_invoice
		)
		Line_item.objects.create(
			line_item='Other Line Item 2',
			line_item_description='Description 2',
			line_item_quantity='2',
			line_item_price='10',
			invoice=other_invoice
		)

		response = self.client.get('/invoices/%d/' % (correct_invoice.id,))
		
		self.assertContains(response, 'Line Item 1')
		self.assertContains(response, 'Line Item 2')

		self.assertNotContains(response, 'Other Line Item 1')
		self.assertNotContains(response, 'Other Line Item 2')

	def test_display_correct_details_for_that_invoice(self):
		correct_invoice = Invoice.objects.create(
			invoice_number='1234',
			invoiced_customer_name='C Name',
			invoiced_customer_address='123 customer address',
			vendors_name='V Name',
			vendors_address='123 vendors address',
			tax_type='TST',
			tax_rate='15'
		)
		Line_item.objects.create(
			line_item='Line Item 1',
			line_item_description='Description 1',
			line_item_quantity='1',
			line_item_price='100',
			invoice=correct_invoice
		)
		other_invoice = Invoice.objects.create()

		Line_item.objects.create(
			line_item='Other Line Item 1',
			line_item_description='Description 1',
			line_item_quantity='1',
			line_item_price='10',
			invoice=other_invoice
		)

		response = self.client.get('/invoices/%d/' % (correct_invoice.id,))

		self.assertContains(response, '123 customer address')
		self.assertContains(response, 'Line Item 1')

		self.assertNotContains(response, 'Other Line Item 1')

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
		first_line_item.line_item_price = '100'
		first_line_item.invoice = invoice_
		first_line_item.save()

		second_line_item = Line_item()
		second_line_item.line_item = 'Item #2'
		second_line_item.line_item_description = 'Description of Item #2'
		second_line_item.line_item_quantity = '1'
		second_line_item.line_item_price = '10'
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
		self.assertIn('10', second_saved_line_item.line_item_price)
		self.assertEqual(second_saved_line_item.line_item_quantity, '1')
		self.assertEqual(second_saved_line_item.line_item_description, 'Description of Item #2')
		self.assertEqual(second_saved_line_item.invoice, invoice_)

	def test_saving_and_retrieving_invoices(self):
		first_invoice = Invoice()
		first_invoice.invoice_number = '1234'
		first_invoice.invoiced_customer_name = 'C Name'
		first_invoice.invoiced_customer_address = '123 customer address'
		first_invoice.vendors_name = 'V Name'
		first_invoice.vendors_address = '123 vendors address'
		first_invoice.tax_type = 'TST'
		first_invoice.tax_rate = '15'
		first_invoice.save()

		second_invoice = Invoice()
		second_invoice.invoice_number = '4321'
		second_invoice.invoiced_customer_name = 'Another C Name'
		second_invoice.invoiced_customer_address = 'Another 123 customer address'
		second_invoice.vendors_name = 'Another V Name'
		second_invoice.vendors_address = 'Another 123 vendors address'
		second_invoice.tax_type = 'TST'
		second_invoice.tax_rate = '15'
		second_invoice.save()

		saved_invoice = Invoice.objects.first()
		self.assertEqual(saved_invoice, first_invoice)

		saved_invoices = Invoice.objects.all()
		self.assertEqual(saved_invoices.count(), 2)

		first_saved_invoice = saved_invoices[0]
		second_saved_invoice = saved_invoices[1]
		self.assertEqual(first_saved_invoice.invoice_number, '1234')
		self.assertEqual(first_saved_invoice.invoiced_customer_name, 'C Name')
		self.assertEqual(first_saved_invoice.invoiced_customer_address, '123 customer address')
		self.assertEqual(first_saved_invoice.vendors_name, 'V Name')
		self.assertEqual(first_saved_invoice.vendors_address, '123 vendors address')
		self.assertEqual(first_saved_invoice.tax_type, 'TST')
		self.assertEqual(first_saved_invoice.tax_rate, '15')
		self.assertEqual(second_saved_invoice.invoice_number, '4321')
		self.assertEqual(second_saved_invoice.invoiced_customer_name, 'Another C Name')

class NewInvoiceTest(TestCase):

	def test_saving_a_POST_request(self):
		self.client.post(
			'/invoices/new',
			data={
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
		)
		self.assertEqual(Line_item.objects.count(), 1)
		new_line_item = Line_item.objects.first()
		self.assertEqual(new_line_item.line_item, 'Item #1')

	def test_redirects_after_POST(self):
		response = self.client.post(
			'/invoices/new',
			data={
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
		)

		self.assertEqual(Line_item.objects.count(), 1)
		new_item = Line_item.objects.first()
		self.assertEqual(new_item.line_item, 'Item #1')
		self.assertEqual(new_item.line_item_price, '100')
		self.assertEqual(new_item.invoice, correct_invoice)

	def test_redirects_to_invoice_view(self):
		other_invoice = Invoice.objects.create()
		correct_invoice = Invoice.objects.create()

		response = self.client.post(
			'/invoices/%d/new_item' % (correct_invoice.id,),
			data={
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
		)
		self.assertRedirects(response, '/invoices/%d/' % (correct_invoice.id,))

class NewCurrencyTest(TestCase):

	def test_can_save_new_currency(self):
		invoice_ = Invoice.objects.create()
		new_currency = Currency.objects.create(
			currency_symbol='$',
			currency_name='CAD',
			invoice=invoice_
		)
		self.assertEqual(Currency.objects.count(), 1)
		new_currency = Currency.objects.first()
		self.assertEqual(new_currency.currency_symbol, '$')
		self.assertEqual(new_currency.currency_name, 'CAD')
		self.assertEqual(new_currency.invoice, invoice_)

	def test_can_save_a_new_currency_in_a_POST_request(self):
		invoice_ = Invoice.objects.create()

		self.client.post(
			'/invoices/new',
			data={
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
		)

		self.assertEqual(Currency.objects.count(), 1)
		new_currency = Currency.objects.first()
		self.assertEqual(new_currency.currency_symbol, '$')
		self.assertEqual(new_currency.currency_name, 'CAD')

	def test_passes_correct_currency_to_template(self):
		correct_invoice = Invoice.objects.create()
		correct_currency = Currency.objects.create(
			currency_symbol='$',
			currency_name='CAD',
			invoice=correct_invoice
		)
		response = self.client.get('/invoices/%d/' % (correct_invoice.id,))
		self.assertEqual(response.context['invoice'], correct_invoice)
		self.assertEqual(response.context['currency'], correct_currency)

class InvoiceAndCurrencyFieldsCanBeUpdated(TestCase):

	def test_invoice_fields_are_updated_on_POST(self):
		self.client.post(
			'/invoices/new',
			data={
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
		)

		self.assertEqual(Invoice.objects.count(), 1)
		new_invoice = Invoice.objects.first()
		self.assertEqual(Line_item.objects.count(), 1)
		new_item = Line_item.objects.first()
		self.assertEqual(new_item.line_item, 'Item #1')
		self.assertEqual(new_item.line_item_price, '100')
		self.assertEqual(new_item.invoice, new_invoice)

		self.client.post(
			'/invoices/%d/new_item' % (new_invoice.id,),
			data={
				'invoice_number': '4321',
				'invoiced_customer_name': 'C Name',
				'invoiced_customer_address': '123 address',
				'vendors_name': 'V Name',
				'vendors_address': '123 address',
				'tax_type': 'TST',
				'tax_rate': '15',
				'currency_symbol': '$',
				'currency_name': 'TST',
				'line_item': 'Item #1',
				'line_item_description': 'Description of Item #1',
				'line_item_quantity': '2',
				'line_item_price': '100'
			}
		)
		
		self.assertEqual(Invoice.objects.count(), 1)
		self.assertEqual(Currency.objects.count(), 1)
		
		updated_invoice = Invoice.objects.get(id=new_invoice.id)
		updated_currency = Currency.objects.get(invoice=updated_invoice)

		self.assertEqual(updated_invoice.invoice_number, '4321')
		self.assertEqual(updated_invoice.tax_type, 'TST')
		self.assertEqual(updated_currency.currency_name, 'TST')

	@skip
	def test_update_invoice_without_adding_new_line_item(self):
		self.client.post(
			'/invoices/new',
			data={
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
		)

		self.assertEqual(Invoice.objects.count(), 1)
		new_invoice = Invoice.objects.first()
		self.assertEqual(Line_item.objects.count(), 1)
		new_item = Line_item.objects.first()
		self.assertEqual(new_item.line_item, 'Item #1')
		self.assertEqual(new_item.line_item_price, '100')
		self.assertEqual(new_item.invoice, new_invoice)

		self.client.post(
			'/invoices/%d/new_item' % (new_invoice.id,),
			data={
				'invoice_number': '4321',
				'invoiced_customer_name': 'C Name',
				'invoiced_customer_address': '123 address',
				'vendors_name': 'V Name',
				'vendors_address': '123 address',
				'tax_type': 'TST',
				'tax_rate': '15',
				'currency_symbol': '$',
				'currency_name': 'TST',
				'line_item': 'Item #2',
				'line_item_description': 'Description of Item #2',
				'line_item_quantity': '2',
				'line_item_price': '100'
			}
		)

		self.assertEqual(Invoice.objects.count(), 1)
		self.assertEqual(Currency.objects.count(), 1)
		
		updated_invoice = Invoice.objects.get(id=new_invoice.id)
		updated_currency = Currency.objects.get(invoice=updated_invoice)

		self.assertEqual(updated_invoice.invoice_number, '4321')
		self.assertEqual(updated_invoice.tax_type, 'TST')
		self.assertEqual(updated_currency.currency_name, 'TST')

		self.client.post(
			'/invoices/%d/new_item' % (new_invoice.id,),
			data={
				'invoice_number': '4321',
				'invoiced_customer_name': 'C Name',
				'invoiced_customer_address': '123 address',
				'vendors_name': 'V Name',
				'vendors_address': '123 address',
				'tax_type': 'TST',
				'tax_rate': '15',
				'currency_symbol': '$',
				'currency_name': 'CST',
			}
		)

		self.assertEqual(Invoice.objects.count(), 1)
		self.assertEqual(Currency.objects.count(), 1)
		
		updated_invoice = Invoice.objects.get(id=new_invoice.id)
		updated_currency = Currency.objects.get(invoice=updated_invoice)

		self.assertEqual(updated_invoice.invoice_number, '4321')
		self.assertEqual(updated_invoice.tax_type, 'TST')
		self.assertEqual(updated_currency.currency_name, 'CST')

		self.assertEqual(2, Line_item.objects.get().count())

class CalculateTotals(TestCase):

	def test_line_item_totals_are_calculated_correctly(self):
		correct_invoice = Invoice.objects.create()

		self.client.post(
			'/invoices/%d/new_item' % (correct_invoice.id,),
			data={
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
		)

		new_item = Line_item.objects.first()
		self.assertEqual(new_item.line_item_total, '200.00')
		
	def test_tax_is_calculated_correctly(self):
		correct_invoice = Invoice.objects.create()

		self.client.post(
			'/invoices/%d/new_item' % (correct_invoice.id,),
			data={
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
		)
		correct_invoice = Invoice.objects.first()
		self.assertEqual(correct_invoice.tax_amount, '30.00')
		

	def test_total_payable_is_calculated_correctly(self):
		correct_invoice = Invoice.objects.create()

		self.client.post(
			'/invoices/%d/new_item' % (correct_invoice.id,),
			data={
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
		)
		correct_invoice = Invoice.objects.first()		
		self.assertEqual(correct_invoice.total_payable, '230.00')

	def test_total_payable_and_tax_amount_are_displayed_after_POST(self):
		correct_invoice = Invoice.objects.create(
			invoice_number='1234',
			invoiced_customer_name='C Name',
			invoiced_customer_address='123 customer address',
			vendors_name='V Name',
			vendors_address='123 vendors address',
			tax_type='TST',
			tax_rate='15'
		)
		new_currency = Currency.objects.create(
			currency_symbol='$',
			currency_name='CAD',
			invoice=correct_invoice
		)
		Line_item.objects.create(
			line_item='Line Item 1',
			line_item_description='Description 1',
			line_item_quantity='1',
			line_item_price='100',
			invoice=correct_invoice
		)
		response = self.client.get('/invoices/%d/' % (correct_invoice.id,))

		self.assertContains(response, '123 customer address')
		self.assertContains(response, 'Line Item 1')
		self.assertContains(response, 'Net: $100.00')
		self.assertContains(response, 'Tax: $15.00')
		self.assertContains(response, 'Total Payable: $115.00')

