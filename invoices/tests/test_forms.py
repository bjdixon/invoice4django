from django.test import TestCase
from invoices.models import Invoice, Currency, Tax, Vendor, Customer, Line_item
from invoices.forms import *
from .utils import *

class InvoiceFormTest(TestCase):

	def test_form_renders_inputs(self):
		form = InvoiceForm()
		self.assertIn('placeholder="Enter an invoice number"', form.as_p())
		self.assertIn('placeholder="Enter any comments, like terms and conditions"', form.as_p())
		self.assertIn('placeholder="Enter date"', form.as_p())
		self.assertIn('class="form-control input-lg"', form.as_p())

		form = CurrencyForm()
		self.assertIn('placeholder="Enter a currency name"', form.as_p())
		self.assertIn('placeholder="Enter the symbol for this currency"', form.as_p())
		self.assertIn('class="form-control input-lg"', form.as_p())

		form = TaxForm()
		self.assertIn('placeholder="Enter a tax type"', form.as_p())
		self.assertIn('placeholder="Enter the tax rate"', form.as_p())
		self.assertIn('class="form-control input-lg"', form.as_p())

	def test_form_validation_for_blank_inputs(self):
		form = InvoiceForm(data={'invoice_number': ''})
		self.assertFalse(form.is_valid())
		self.assertEqual(form.errors['invoice_number'], [EMPTY_INVOICE_NUMBER_ERROR])

	def test_form_handles_saving_to_invoice(self):
		form = InvoiceForm(data={
			'invoice_number': '1234',
			'invoice_date': '03/12/2013',
			'invoice_comment': 'Please pay up'
		})
		invoice_ = form.save()
		self.assertEqual(invoice_.invoice_number, '1234')
		self.assertEqual(invoice_.invoice_comment, 'Please pay up')

		form = CurrencyForm(data={
			'currency_name': 'USD',
			'currency_symbol': '$'
		})
		currency_ = form.save(invoice=invoice_)
		self.assertEqual(currency_.currency_name, 'USD')
		self.assertEqual(currency_.currency_symbol, '$')

		form = TaxForm(data={
			'tax_name': 'TST',
			'tax_rate': '25'
		})
		tax_ = form.save(invoice=invoice_)
		self.assertEqual(tax_.tax_name, 'TST')
		self.assertEqual(tax_.tax_rate, 25)

	
class VendorFormTest(TestCase):

	def test_form_renders_inputs(self):
		form = VendorForm()
		self.assertIn('placeholder="Enter your company name"', form.as_p())
		self.assertIn('placeholder="Enter your street address"', form.as_p())
		self.assertIn('placeholder="Enter your city"', form.as_p())
		self.assertIn('placeholder="Enter your state"', form.as_p())
		self.assertIn('placeholder="Enter your postal code"', form.as_p())
		self.assertIn('placeholder="Enter your phone number"', form.as_p())
		self.assertIn('placeholder="Enter your email address"', form.as_p())
		self.assertIn('class="form-control input-lg"', form.as_p())

	def test_form_validation_for_blank_inputs(self):
		form = VendorForm({
			'vendor_name': '',
			'vendor_street_address': '',
			'vendor_city': '',
			'vendor_state': '',
			'vendor_post_code': '',
			'vendor_email_address': ''
		})
		self.assertFalse(form.is_valid())
		self.assertEqual(form.errors['vendor_name'], [EMPTY_NAME_ERROR])
		self.assertEqual(form.errors['vendor_street_address'], [EMPTY_STREET_ADDRESS_ERROR])
		self.assertEqual(form.errors['vendor_city'], [EMPTY_CITY_ERROR])
		self.assertEqual(form.errors['vendor_state'], [EMPTY_STATE_ERROR])
		self.assertEqual(form.errors['vendor_post_code'], [EMPTY_POST_CODE_ERROR])
		self.assertEqual(form.errors['vendor_phone_number'], [EMPTY_PHONE_NUMBER_ERROR])
		self.assertEqual(form.errors['vendor_email_address'],[EMPTY_EMAIL_ADDRESS_ERROR])

	def test_form_handles_saving_to_vendor(self):
		invoice_ = create_new_invoice()
		form = VendorForm(data={
			'vendor_name': 'V Name',
			'vendor_street_address': '123 vendor street',
			'vendor_city': 'Vendor City',
			'vendor_state': 'VS',
			'vendor_post_code': 'Vendor',
			'vendor_phone_number': '123 123 1234',
			'vendor_email_address': 'vendor@email.com'
		})
		vendor_ = form.save(invoice=invoice_)
		self.assertEqual(vendor_.vendor_name, 'V Name')
		self.assertEqual(vendor_.vendor_street_address, '123 vendor street')
		self.assertEqual(vendor_.vendor_city, 'Vendor City')
		self.assertEqual(vendor_.vendor_state, 'VS')
		self.assertEqual(vendor_.vendor_post_code, 'Vendor')
		self.assertEqual(vendor_.vendor_phone_number, '123 123 1234')
		self.assertEqual(vendor_.vendor_email_address, 'vendor@email.com')


class CustomerFormTest(TestCase):

	def test_form_renders_inputs(self):
		form = CustomerForm()
		self.assertIn('placeholder="Enter customer company name"', form.as_p())
		self.assertIn('placeholder="Enter customer street address"', form.as_p())
		self.assertIn('placeholder="Enter customer city"', form.as_p())
		self.assertIn('placeholder="Enter customer state"', form.as_p())
		self.assertIn('placeholder="Enter customer postal code"', form.as_p())
		self.assertIn('placeholder="Enter customer phone number"', form.as_p())
		self.assertIn('placeholder="Enter customer email address"', form.as_p())
		self.assertIn('class="form-control input-lg"', form.as_p())

	def test_form_validation_for_blank_inputs(self):
		form = CustomerForm({
			'customer_name': '',
			'customer_street_address': '',
			'customer_city': '',
			'customer_state': '',
			'customer_post_code': '',
			'customer_email_address': ''
		})
		self.assertFalse(form.is_valid())
		self.assertEqual(form.errors['customer_name'], [EMPTY_NAME_ERROR])
		self.assertEqual(form.errors['customer_street_address'], [EMPTY_STREET_ADDRESS_ERROR])
		self.assertEqual(form.errors['customer_city'], [EMPTY_CITY_ERROR])
		self.assertEqual(form.errors['customer_state'],[EMPTY_STATE_ERROR])
		self.assertEqual(form.errors['customer_post_code'], [EMPTY_POST_CODE_ERROR])
		self.assertEqual(form.errors['customer_phone_number'], [EMPTY_PHONE_NUMBER_ERROR])
		self.assertEqual(form.errors['customer_email_address'], [EMPTY_EMAIL_ADDRESS_ERROR])

	def test_form_handles_saving_to_customer(self):
		invoice_ = create_new_invoice()	
		form = CustomerForm(data={
			'customer_name': 'C Name',
			'customer_street_address': '123 customer street',
			'customer_city': 'Customer City',
			'customer_state': 'CS',
			'customer_post_code': 'Customer',
			'customer_phone_number': '123 123 1234',
			'customer_email_address': 'customer@email.com'
		})
		customer_ = form.save(invoice=invoice_)
		self.assertEqual(customer_.customer_name, 'C Name')
		self.assertEqual(customer_.customer_street_address, '123 customer street')
		self.assertEqual(customer_.customer_city, 'Customer City')
		self.assertEqual(customer_.customer_state, 'CS')
		self.assertEqual(customer_.customer_post_code, 'Customer')
		self.assertEqual(customer_.customer_phone_number, '123 123 1234')
		self.assertEqual(customer_.customer_email_address, 'customer@email.com')

class LineItemFormTest(TestCase):

	def test_form_renders_inputs(self):
		form = LineItemForm()
		self.assertIn('placeholder="Enter a line item"', form.as_p())
		self.assertIn('placeholder="Enter a description"', form.as_p())
		self.assertIn('placeholder="Enter the quantity"', form.as_p())
		self.assertIn('placeholder="Enter the price per item"', form.as_p())

	def test_form_validation_for_blank_inputs(self):
		form = LineItemForm(data={
			'line_item': '',
			'line_item_quantity': '',
			'line_item_price': ''
		})
		self.assertFalse(form.is_valid())
		self.assertEqual(form.errors['line_item'], [EMPTY_LINE_ITEM_ERROR])
		self.assertEqual(form.errors['line_item_quantity'], [EMPTY_LINE_ITEM_QUANTITY_ERROR])
		self.assertEqual(form.errors['line_item_price'], [EMPTY_LINE_ITEM_PRICE_ERROR])

	def test_form_handles_saving_to_line_item(self):
		invoice_ = create_new_invoice()
		form = LineItemForm(data={
			'line_item': 'Item 1',
			'line_item_description': 'Description 1',
			'line_item_quantity': 1,
			'line_item_price': 100
		})
		line_item_ = form.save(invoice=invoice_)
		self.assertEqual(line_item_.line_item, 'Item 1')
		self.assertEqual(line_item_.line_item_description, 'Description 1')
		self.assertEqual(line_item_.line_item_quantity, 1)
		self.assertEqual(line_item_.line_item_price, 100)

