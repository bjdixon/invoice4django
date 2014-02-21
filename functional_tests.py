from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_can_start_an_invoice_and_retrieve_it_later(self):
		# Jolby has heard about a new invoice site. He goes
		# to check out it's home page.
		self.browser.get('http://localhost:8000')

		# he notices the page title and header mention Invoices
		self.assertIn('Invoices', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('Invoices', header_text)

		# he is invited to enter an invoice number
		invoice_number_input = self.browser.find_element_by_id('invoice_number_input')
		self.assertEqual(
			invoice_number_input.get_attribute('placeholder'),
			'Enter the invoice number'
		)
		invoice_number_input.send_keys('1234')

		# he is invited to enter a customer and their address
		invoiced_customer_name_input = self.browser.find_element_by_id('invoiced_customer_name_input')
		invoiced_customer_address_input = self.browser.find_element_by_id('invoiced_customer_address_input')
		self.assertEqual(
			invoiced_customer_name_input.get_attribute('placeholder'),
			'Enter a customer'
		)
		self.assertEqual(
			invoiced_customer_address_input.get_attribute('placeholder'),
			'Enter customer address'
		)
		invoiced_customer_name_input.send_keys('Bob Buyer')
		invoiced_customer_address_input.send_keys('123 anystreet, anytown')

		# he is invited to enter his own name and address
		vendors_name_input = self.browser.find_element_by_id('vendors_name_input')
		vendors_address_input = self.browser.find_element_by_id('vendors_address_input')
		self.assertEqual(
			vendors_name_input.get_attribute('placeholder'),
			'Enter your name'
		)
		self.assertEqual(
			vendors_address_input.get_attribute('placeholder'),
			'Enter your address'
		)
		vendors_name_input.send_keys('my name')
		vendors_address_input.send_keys('my address, my town')

		# he is invited to add a tax type and tax percentage
		tax_type_input = self.browser.find_element_by_id('tax_type_input')
		tax_rate_input = self.browser.find_element_by_id('tax_rate_input')
		self.assertEqual(
			tax_type_input.get_attribute('placeholder'),
			'Enter tax name'
		)
		self.assertEqual(
			tax_rate_input.get_attribute('placeholder'),
			'Enter tax rate'
		)
		tax_type_input.send_keys('AST')
		tax_rate_input.send_keys('25')

		# he is invited to add a line item, description, price and quantity
		line_item_input = self.browser.find_element_by_id('line_item_input')
		line_item_description_input = self.browser.find_element_by_id('line_item_description_input')
		line_item_price_input = self.browser.find_element_by_id('line_item_price_input')
		line_item_quantity_input = self.browser.find_element_by_id('line_item_quantity_input')
		self.assertEqual(
			line_item_input.get_attribute('placeholder'),
			'Enter a line item'
		)
		self.assertEqual(
			line_item_description_input.get_attribute('placeholder'),
			'Enter line item description'
		)
		self.assertEqual(
			line_item_price_input.get_attribute('placeholder'),
			'Enter price per item'
		)
		self.assertEqual(
			line_item_quantity_input.get_attribute('placeholder'),
			'Enter quantity'
		)
		line_item_input.send_keys('Item #1')
		line_item_description_input.send_keys('Description of item #1')
		line_item_price_input.send_keys('45.00')
		line_item_quantity_input.send_keys('2')
		self.browser.find_element_by_tag_name('button').send_keys(Keys.ENTER)

		# After hitting enter he notices the page updates showing the entered values
		# and new inputs for another line item
		table = self.browser.find_element_by_id('invoice_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn('Invoice Number: 1234', [row.text for row in rows])
		self.assertIn('Customer: Bob Buyer', [row.text for row in rows])
		self.assertIn('Customer address: 123 anystreet, anytown', [row.text for row in rows])
		self.assertIn('Vendors name: my name', [row.text for row in rows])
		self.assertIn('Vendors address: my address, my town', [row.text for row in rows])
		self.assertIn('Tax type: AST', [row.text for row in rows])
		self.assertIn('Tax rate: 25', [row.text for row in rows])

		# ALSO NEED TO CHECK THAT PAYEE, NAME, ADDRESS, TAX STUFF IS DISPLAYED!
		# PAGE 63 SAVING USER INPUT

		# he notices that he can add more line items and delete previously added
		# line items


		# he notices that after each line item is added the net, tax and total 
		# payable amounts increase by the correct amount


		# he notices that he can click a button to save the invoice as a pdf 


		# he notices that he can enter the customer's email address and send the 
		# invoice directly to them.


		self.fail('finish the test')


if __name__ == '__main__':
	unittest.main(warnings='ignore')


