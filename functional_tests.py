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
		invoice_number_input = self.browser.find_element_by_id('invoice_number')
		self.assertEqual(
			invoice_number_input.get_attribute('placeholder'),
			'Enter the invoice number'
		)

		# he is invited to enter a payee and their address
		invoiced_payee_input = self.browser.find_element_by_id('invoiced_payee_input')
		invoiced_payee_address_input = self.browser.find_element_by_id('invoiced_payee_address_input')
		self.assertEqual(
			invoiced_payee_input.get_attribute('placeholder'),
			'Enter a payee'
		)
		self.assertEqual(
			invoiced_payee_address_input.get_attribute('placeholder'),
			'Enter payee address'
		)
		invoiced_payee_input.send_keys('Bob Buyer')
		invoiced_payee_address_input.send_keys('123 anystreet, anytown')

		# he is invited to enter his own name and address
		name_input = self.browser.find_element_by_id('name_input')
		address_input = self.browser.find_element_by_id('address_input')
		self.assertEqual(
			name_input.get_attribute('placeholder'),
			'Enter your name'
		)
		self.assertEqual(
			address_input.get_attribute('placeholder'),
			'Enter your address'
		)
		name_input.send_keys('my name')
		address_input.send_keys('my address, my town')

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


		# he notices that he can add more line items and delete previously added
		# line items


		# he notices that after each line item is added the net, tax and total 
		# payable amounts increase by the correct amount


		# he notices that he can click a button to save the invoice as a pdf 


		# he notices that he can enter the payee's email address and send the 
		# invoice directly to them.


		self.fail('finish the test')


if __name__ == '__main__':
	unittest.main(warnings='ignore')


