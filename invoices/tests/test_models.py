import time
import datetime
from django.test import TestCase
from django.core.exceptions import ValidationError
from unittest import skip

from invoices.models import Invoice, Line_item, Currency, Vendor, Customer, Tax
from .utils import create_new_invoice, create_new_line_item, create_new_vendor, create_new_customer, create_new_tax, create_new_currency


class CreateAndRetrieveModelObjects(TestCase):

	def test_creating_invoice(self):
		new_invoice = create_new_invoice()
		saved_invoice = Invoice.objects.first()
		self.assertEqual(new_invoice.id, saved_invoice.id)
		
	def test_creating_currency(self):
		invoice_ = create_new_invoice()
		new_currency = create_new_currency(invoice=invoice_)
		saved_currency = Currency.objects.first()
		self.assertEqual(new_currency, saved_currency)
		
	def test_creating_tax(self):
		invoice_ = create_new_invoice()
		new_tax = create_new_tax(invoice=invoice_)
		saved_tax = Tax.objects.first()
		self.assertEqual(new_tax, saved_tax)
		
	def test_creating_vendor(self):
		new_vendor = create_new_vendor()
		saved_vendor = Vendor.objects.first()
		self.assertEqual(new_vendor, saved_vendor)
		
	def test_creating_customer(self):
		new_customer = create_new_customer()
		saved_customer = Customer.objects.first()
		self.assertEqual(new_customer, saved_customer)
		
	def test_creating_line_item(self):
		invoice_ = create_new_invoice()
		new_line_item = create_new_line_item(invoice=invoice_)
		saved_line_item = Line_item.objects.first()
		self.assertEqual(new_line_item, saved_line_item)
		
		
class UpdateModelObjects(TestCase):
	
	def test_updating_invoice(self):
		new_invoice = create_new_invoice()
		saved_invoice = Invoice.objects.first()
		saved_invoice.invoice_number = '5555'
		saved_invoice.invoice_date = datetime.date(2014, 1, 1)
		saved_invoice.invoice_comment = 'New comment'
		saved_invoice.save()
		self.assertEqual(Invoice.objects.count(), 1)
		updated_invoice = Invoice.objects.first()
		self.assertEqual(updated_invoice.invoice_number, '5555')
		self.assertEqual(updated_invoice.invoice_date, datetime.date(2014, 1, 1))
		self.assertEqual(updated_invoice.invoice_comment, 'New comment')
		
	def test_updating_currency(self):
		invoice_ = create_new_invoice()
		new_currency = create_new_currency(invoice=invoice_)
		saved_currency = Currency.objects.first()
		saved_currency.currency_name = 'CAD'
		saved_currency.currency_symbol = '&'
		saved_currency.save()
		self.assertEqual(Currency.objects.count(), 1)
		updated_currency = Currency.objects.first()
		self.assertEqual(updated_currency.currency_name, 'CAD')
		self.assertEqual(updated_currency.currency_symbol, '&')
		
	def test_updating_tax(self):
		invoice_ = create_new_invoice()
		new_tax = create_new_tax(invoice=invoice_)
		saved_tax = Tax.objects.first()
		saved_tax.tax_rate = 25
		saved_tax.tax_name = 'HST'
		saved_tax.save()
		self.assertEqual(Tax.objects.count(), 1)
		updated_tax = Tax.objects.first()
		self.assertEqual(updated_tax.tax_rate, 25)
		self.assertEqual(updated_tax.tax_name, 'HST')
		
	def test_updating_vendor(self):
		new_vendor = create_new_vendor()
		saved_vendor = Vendor.objects.first()
		saved_vendor.vendor_name = 'New name'
		saved_vendor.vendor_street_address = 'New street address'
		saved_vendor.vendor_city = 'New City'
		saved_vendor.vendor_state = 'NS'
		saved_vendor.vendor_post_code = 'New code'
		saved_vendor.vendor_phone_number = '555 555 5555'
		saved_vendor.vendor_email_address = 'new@email.com'
		saved_vendor.save()
		self.assertEqual(Vendor.objects.count(), 1)
		updated_vendor = Vendor.objects.first()
		self.assertEqual(updated_vendor.vendor_name, 'New name')
		self.assertEqual(updated_vendor.vendor_street_address, 'New street address')
		self.assertEqual(updated_vendor.vendor_city, 'New City')
		self.assertEqual(updated_vendor.vendor_state, 'NS')
		self.assertEqual(updated_vendor.vendor_post_code, 'New code')
		self.assertEqual(updated_vendor.vendor_phone_number, '555 555 5555')
		self.assertEqual(updated_vendor.vendor_email_address, 'new@email.com')
		
	def test_updating_customer(self):
		new_customer = create_new_customer()
		saved_customer = Customer.objects.first()
		saved_customer.customer_name = 'New name'
		saved_customer.customer_street_address = 'New street address'
		saved_customer.customer_city = 'New City'
		saved_customer.customer_state = 'NS'
		saved_customer.customer_post_code = 'New code'
		saved_customer.customer_phone_number = '555 555 5555'
		saved_customer.customer_email_address = 'new@email.com'
		saved_customer.save()
		self.assertEqual(Customer.objects.count(), 1)
		updated_customer = Customer.objects.first()
		self.assertEqual(updated_customer.customer_name, 'New name')
		self.assertEqual(updated_customer.customer_street_address, 'New street address')
		self.assertEqual(updated_customer.customer_city, 'New City')
		self.assertEqual(updated_customer.customer_state, 'NS')
		self.assertEqual(updated_customer.customer_post_code, 'New code')
		self.assertEqual(updated_customer.customer_phone_number, '555 555 5555')
		self.assertEqual(updated_customer.customer_email_address, 'new@email.com')
		
	def test_updating_line_item(self):
		invoice_ = create_new_invoice()
		new_line_item = create_new_line_item(invoice=invoice_)
		saved_line_item = Line_item.objects.first()
		saved_line_item.line_item = 'New item'
		saved_line_item.line_item_description = 'Description of line item'
		saved_line_item.line_item_price = 300
		saved_line_item.line_item_quantity = 10
		saved_line_item.save()
		self.assertEqual(Line_item.objects.count(), 1)
		updated_line_item = Line_item.objects.first()
		self.assertEqual(updated_line_item.line_item, 'New item')
		self.assertEqual(updated_line_item.line_item_description, 'Description of line item')
		self.assertEqual(updated_line_item.line_item_price, 300)
		self.assertEqual(updated_line_item.line_item_quantity, 10)
		
	def test_invoice_can_have_multiple_taxes(self):
		invoice_ = create_new_invoice()
		first_new_tax = create_new_tax(invoice=invoice_)
		second_new_tax = create_new_tax(invoice=invoice_)
		self.assertEqual(Tax.objects.filter(invoice=invoice_).count(), 2)
		self.assertNotEqual(first_new_tax, second_new_tax)
		
	def test_invoice_can_have_multiple_line_items(self):
		invoice_ = create_new_invoice()
		first_new_line_item = create_new_line_item(invoice=invoice_)
		second_new_line_item = create_new_line_item(invoice=invoice_)
		self.assertEqual(Line_item.objects.filter(invoice=invoice_).count(), 2)
		self.assertNotEqual(first_new_line_item, second_new_line_item)
		
	
class DeleteModelObjects(TestCase):

	def test_delete_invoice(self):
		''' If an invoice is deleted all associated currency, tax, customer 
		    and line item objects should be deleted
		     as well or they'll become orphans '''
		invoice_ = create_new_invoice()
		new_currency = create_new_currency(invoice=invoice_)
		first_new_tax = create_new_tax(invoice=invoice_)
		new_line_item = create_new_line_item(invoice=invoice_)
		new_customer = create_new_customer()
		new_customer.invoice = invoice_
		new_customer.save()
		invoice_.delete()
		self.assertEqual(Currency.objects.count(), 0)
		self.assertEqual(Tax.objects.count(), 0)
		self.assertEqual(Line_item.objects.count(), 0)
		self.assertEqual(Customer.objects.count(), 0)
		
	def test_delete_currency(self):
		invoice_ = create_new_invoice()
		new_currency = create_new_currency(invoice=invoice_)
		Currency.objects.filter(invoice=invoice_).delete()
		self.assertEqual(Currency.objects.count(), 0)
		
	def test_delete_all_taxes_for_an_invoice(self):
		invoice_ = create_new_invoice()
		first_tax = create_new_tax(invoice=invoice_)
		second_tax = create_new_tax(invoice=invoice_)
		Tax.objects.filter(invoice=invoice_).delete()
		self.assertEqual(Tax.objects.count(), 0)
		
	def test_delete_individual_tax(self):
		invoice_ = create_new_invoice()
		first_tax = create_new_tax(invoice=invoice_)
		second_tax = create_new_tax(invoice=invoice_)
		Tax.objects.filter(id=first_tax.id).delete()
		self.assertEqual(Tax.objects.filter(invoice=invoice_).count(), 1)
		
	def test_delete_vendor(self):
		invoice_ = create_new_invoice()
		new_vendor = create_new_vendor()
		new_vendor.invoice = invoice_
		new_vendor.save()
		Vendor.objects.filter(invoice=invoice_).delete()
		self.assertEqual(Vendor.objects.count(), 0)
		
	def test_delete_customer(self):
		invoice_ = create_new_invoice()
		new_customer = create_new_customer()
		new_customer.invoice = invoice_
		new_customer.save()
		Customer.objects.filter(invoice=invoice_).delete()
		self.assertEqual(Customer.objects.count(), 0)
		
	def test_delete_all_line_items_for_an_invoice(self):
		invoice_ = create_new_invoice()
		first_line_item = create_new_line_item(invoice=invoice_)
		second_line_item = create_new_line_item(invoice=invoice_)
		Line_item.objects.filter(invoice=invoice_).delete()
		self.assertEqual(Line_item.objects.count(), 0)
		
	def test_delete_individual_line_item(self):
		invoice_ = create_new_invoice()
		first_line_item = create_new_line_item(invoice=invoice_)
		second_line_item = create_new_line_item(invoice=invoice_)
		Line_item.objects.filter(id=first_line_item.id).delete()
		self.assertEqual(Line_item.objects.count(), 1)
	

class CalculatingTaxAndTotalsInTheModel(TestCase):

	def test_line_item_totals_are_calculated_correctly(self):
		invoice_ = create_new_invoice()
		new_line_item = create_new_line_item(invoice=invoice_)
		self.assertEqual(new_line_item.get_line_item_total(), 100)
		
	def test_net_total_for_an_invoice_is_calculated_correctly(self):
		invoice_ = create_new_invoice()
		first_line_item = create_new_line_item(invoice=invoice_)
		second_line_item = create_new_line_item(invoice=invoice_)
		self.assertEqual(invoice_.get_net_total(), 200)
		
	def test_tax_is_correctly_calculated(self):
		invoice_ = create_new_invoice()
		tax = create_new_tax(invoice=invoice_)
		new_line_item = create_new_line_item(invoice=invoice_)
		self.assertEqual(invoice_.get_tax_total(), 15)
		
	def test_total_payable_is_calculated_correctly(self):
		invoice_ = create_new_invoice()
		first_tax = create_new_tax(invoice=invoice_)
		second_tax = create_new_tax(invoice=invoice_)
		first_line_item = create_new_line_item(invoice=invoice_)
		second_line_item = create_new_line_item(invoice=invoice_)
		self.assertEqual(invoice_.get_total_payable(), 260)
		





