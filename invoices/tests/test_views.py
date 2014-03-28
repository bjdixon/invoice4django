from django.core.urlresolvers import resolve
from django.test import TestCase
from unittest import skip
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape


class HomePageTest(TestCase):
	@skip
	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)
	@skip
	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)
	@skip
	def test_home_page_renders_home_template(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')


class InvoiceViewTest(TestCase):
	@skip
	def test_uses_invoice_template(self):
		invoice_ = create_new_invoice()
		response = self.client.get('/invoices/%d/' % (invoice_.id,))
		self.assertTemplateUsed(response, 'invoice.html')
	@skip
	def test_display_only_items_for_that_invoice(self):
		correct_invoice = create_new_invoice()
		create_new_line_item(invoice_=correct_invoice)	
		create_new_line_item(invoice_=correct_invoice, num='2')	
		
		other_invoice = create_new_invoice()

		create_new_line_item(invoice_=other_invoice, num='3')
		create_new_line_item(invoice_=other_invoice, num='4')
		response = self.client.get('/invoices/%d/' % (correct_invoice.id,))
		
		self.assertContains(response, 'Line Item 1')
		self.assertContains(response, 'Line Item 2')

		self.assertNotContains(response, 'Line Item 3')
		self.assertNotContains(response, 'Line Item 4')
	@skip
	def test_display_correct_details_for_that_invoice(self):
		correct_invoice = create_new_invoice()
		create_new_line_item(invoice_=correct_invoice)	

		other_invoice = create_new_invoice(alt=1)
		create_new_line_item(invoice_=other_invoice, num='2')

		response = self.client.get('/invoices/%d/' % (correct_invoice.id,))

		self.assertContains(response, '123 customer address')
		self.assertContains(response, 'Line Item 1')

		self.assertNotContains(response, 'Line Item 2')
	@skip
	def test_passes_correct_invoice_to_template(self):
		other_invoice = create_new_invoice()
		correct_invoice = create_new_invoice(alt=1)
		response = self.client.get('/invoices/%d/' % (correct_invoice.id,))
		self.assertEqual(response.context['invoice'], correct_invoice)


class InvoiceAndLineItemModelTest(TestCase):
	@skip
	def test_saving_and_retrieving_line_items(self):
		correct_invoice = create_new_invoice()
		first_line_item = create_new_line_item(invoice_=correct_invoice)
		second_line_item = create_new_line_item(invoice_=correct_invoice, num='2')
		
		saved_invoice = Invoice.objects.first()
		self.assertEqual(saved_invoice, correct_invoice)

		saved_line_items = Line_item.objects.all()
		self.assertEqual(saved_line_items.count(), 2)

		first_saved_line_item = saved_line_items[0]
		second_saved_line_item = saved_line_items[1]
		self.assertEqual(first_saved_line_item.line_item, 'Line Item 1')
		self.assertEqual(first_saved_line_item.invoice, correct_invoice)
		self.assertEqual(second_saved_line_item.line_item, 'Line Item 2')
		self.assertIn('200', second_saved_line_item.line_item_price)
		self.assertEqual(second_saved_line_item.line_item_quantity, '2')
		self.assertEqual(second_saved_line_item.line_item_description, 'Description 2')
		self.assertEqual(second_saved_line_item.invoice, correct_invoice)
	@skip
	def test_saving_and_retrieving_invoices(self):
		first_invoice = create_new_invoice()
		second_invoice = create_new_invoice(alt=1)

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
		self.assertEqual(second_saved_invoice.invoiced_customer_address, '123 another customer address')
		self.assertEqual(second_saved_invoice.vendors_address, '123 another vendors address')

class NewInvoiceTest(TestCase):
	@skip
	def test_saving_a_POST_request(self):
		self.client.post(
			'/invoices/new',
			data=create_POST_data()
		)
		self.assertEqual(Line_item.objects.count(), 1)
		new_line_item = Line_item.objects.first()
		self.assertEqual(new_line_item.line_item, 'Item #1')
	@skip
	def test_redirects_after_POST(self):
		response = self.client.post(
			'/invoices/new',
			data=create_POST_data()
		)
		new_invoice = Invoice.objects.first()
		self.assertRedirects(response, '/invoices/%d/' % (new_invoice.id,))
	@skip
	def test_validation_errors_sent_back_to_home_page_template(self):
		response = self.client.post(
			'/invoices/new',
			data={
				'invoice_number': '',
				'invoiced_customer_name': '',
				'invoiced_customer_address': '',
				'vendors_name': '',
				'vendors_address': '',
				'tax_type': '',
				'tax_rate': '',
			}
		)
		self.assertEqual(Invoice.objects.all().count(), 0)
		self.assertTemplateUsed(response, 'home.html')
		expected_error = escape("You can't save an empty invoice")
		self.assertContains(response, expected_error)


class NewItemTest(TestCase):
	@skip
	def test_can_save_a_POST_request_to_an_existing_invoice(self):
		other_invoice = create_new_invoice()
		correct_invoice = create_new_invoice()

		self.client.post(
			'/invoices/%d/new_item' % (correct_invoice.id,),
			data=create_POST_data()
		)

		self.assertEqual(Line_item.objects.count(), 1)
		new_item = Line_item.objects.first()
		self.assertEqual(new_item.line_item, 'Item #1')
		self.assertEqual(new_item.line_item_price, '100')
		self.assertEqual(new_item.invoice, correct_invoice)
	@skip
	def test_redirects_to_invoice_view(self):
		other_invoice = create_new_invoice()
		correct_invoice = create_new_invoice()

		response = self.client.post(
			'/invoices/%d/new_item' % (correct_invoice.id,),
			data=create_POST_data()
		)
		self.assertRedirects(response, '/invoices/%d/' % (correct_invoice.id,))

class NewCurrencyTest(TestCase):
	@skip
	def test_can_save_new_currency(self):
		invoice_ = create_new_invoice()
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
	@skip
	def test_can_save_a_new_currency_in_a_POST_request(self):
		invoice_ = create_new_invoice()

		self.client.post(
			'/invoices/new',
			data=create_POST_data()
		)

		self.assertEqual(Currency.objects.count(), 1)
		new_currency = Currency.objects.first()
		self.assertEqual(new_currency.currency_symbol, '$')
		self.assertEqual(new_currency.currency_name, 'CAD')
	@skip
	def test_passes_correct_currency_to_template(self):
		correct_invoice = create_new_invoice()
		correct_currency = Currency.objects.create(
			currency_symbol='$',
			currency_name='CAD',
			invoice=correct_invoice
		)
		response = self.client.get('/invoices/%d/' % (correct_invoice.id,))
		self.assertEqual(response.context['invoice'], correct_invoice)
		self.assertEqual(response.context['currency'], correct_currency)

class InvoiceAndCurrencyFieldsCanBeUpdated(TestCase):
	@skip
	def test_invoice_fields_are_updated_on_POST(self):
		self.client.post(
			'/invoices/new',
			data=create_POST_data()
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
			data=create_POST_data()
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
				'currency_name': 'TST'
			}
		)

		self.assertEqual(Invoice.objects.count(), 1)
		self.assertEqual(Currency.objects.count(), 1)
		self.assertEqual(Line_item.objects.count(), 1)
		
		updated_invoice = Invoice.objects.get(id=new_invoice.id)
		updated_currency = Currency.objects.get(invoice=updated_invoice)

		self.assertEqual(updated_invoice.invoice_number, '4321')
		self.assertEqual(updated_invoice.tax_type, 'TST')
		self.assertEqual(updated_currency.currency_name, 'TST')


class CalculateTotals(TestCase):
	@skip
	def test_line_item_totals_are_calculated_correctly(self):
		correct_invoice = create_new_invoice()

		self.client.post(
			'/invoices/%d/new_item' % (correct_invoice.id,),
			data=create_POST_data()
		)

		new_item = Line_item.objects.first()
		self.assertEqual(new_item.line_item_total, '200.00')
	@skip	
	def test_tax_is_calculated_correctly(self):
		correct_invoice = create_new_invoice()

		self.client.post(
			'/invoices/%d/new_item' % (correct_invoice.id,),
			data=create_POST_data()
		)
		correct_invoice = Invoice.objects.first()
		self.assertEqual(correct_invoice.tax_amount, '30.00')
	@skip
	def test_total_payable_is_calculated_correctly(self):
		correct_invoice = create_new_invoice()

		self.client.post(
			'/invoices/%d/new_item' % (correct_invoice.id,),
			data=create_POST_data()
		)
		correct_invoice = Invoice.objects.first()		
		self.assertEqual(correct_invoice.total_payable, '230.00')
	@skip
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
	@skip
	def test_total_payable_and_tax_amount_are_updated_after_changes_to_invoice(self):
		invoice_ = create_new_invoice()
		line_item = create_new_line_item(invoice_=invoice_)
		
		self.client.post(
			'/invoices/new',
			data=create_POST_data()
		)
		
		invoice_ = Invoice.objects.first()
		self.assertEqual(invoice_.tax_rate, '15')
		self.assertEqual(invoice_.total_payable, '115.00')

		self.client.post(
			'/invoices/%d/new_item' % (invoice_.id,),
			data={
				'invoice_number': '1234',
				'invoiced_customer_name': 'C Name',
				'invoiced_customer_address': '123 address',
				'vendors_name': 'V Name',
				'vendors_address': '123 address',
				'tax_type': 'TST',
				'tax_rate': '20',
				'currency_symbol': '$',
				'currency_name': 'TST'
			}
		)

		invoice_ = Invoice.objects.first()
		self.assertEqual(invoice_.tax_rate, '20')
		self.assertEqual(invoice_.total_payable, '120.00')


