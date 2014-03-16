from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError

from invoices.views import home_page
from invoices.models import Invoice, Line_item, Currency


class CreatingAndRetrievingModels(TestCase):

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


class UpdatingModels(TestCase):
	
	def test_invoice_fields_can_be_overwritten(self):
		invoice_ = Invoice.objects.create(
			invoice_number=1234,
			invoiced_customer_name='name',
			invoiced_customer_address='address',
			vendors_name='vname',
			vendors_address='vaddress',
			tax_type='TST',
			tax_rate='25'
		)

		self.assertEqual(Invoice.objects.count(), 1)
		self.assertEqual(Invoice.objects.first(), invoice_)

		updated_invoice = Invoice.objects.first()
		updated_invoice.tax_type = 'TAX'
		updated_invoice.vendor_name = 'new name'
		updated_invoice.save()

		self.assertEqual(Invoice.objects.first(), updated_invoice)
		edited_invoice = Invoice.objects.first()
		self.assertEqual(edited_invoice.tax_type, 'TAX')
		self.assertEqual(edited_invoice.vendors_name, updated_invoice.vendors_name)

	def test_currency_fields_can_be_overwritten(self):
		invoice_ = Invoice.objects.create()
		currency_ = Currency.objects.create(
			currency_symbol='$',
			currency_name='CAD',
			invoice=invoice_
		)

		self.assertEqual(Currency.objects.count(), 1)
		self.assertEqual(Currency.objects.first(), currency_)
		
		update_currency = Currency.objects.first()
		update_currency.currency_name = 'TST'
		update_currency.save()

		edited_currency = Currency.objects.first()

		self.assertEqual(Currency.objects.count(), 1)
		self.assertEqual(edited_currency.invoice, invoice_)
		self.assertEqual(edited_currency.currency_name, 'TST')


class ModelValidation(TestCase):

	def test_cant_add_empty_invoice(self):
		invoice_ = Invoice()
		with self.assertRaises(ValidationError):
			invoice_.save()
		
