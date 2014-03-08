from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):


	def test_can_start_an_invoice_and_retrieve_it_later(self):
		# Jolby has heard about a new invoice site. He goes
		# to check out it's home page.
		self.browser.get(self.live_server_url)

		# he notices the page title and header mention Invoices
		self.assertIn('Invoices', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('Invoice', header_text)

		# he is invited to enter an invoice number
		invoice_number = self.browser.find_element_by_id('new_invoice_number_input')
		invoice_number.send_keys('1234')

		# he is invited to enter a customer and their address
		customer_name = self.browser.find_element_by_id('new_invoiced_customer_name_input')
		customer_name.send_keys('Mr Customer')

		customer_address = self.browser.find_element_by_id('new_invoiced_customer_address_input')
		customer_address.send_keys('123 street name, anytown')

		# he is invited to enter his own name and address
		vendors_name = self.browser.find_element_by_id('new_vendors_name_input')
		vendors_name.send_keys('Jolby')

		vendors_address = self.browser.find_element_by_id('new_vendors_address_input')
		vendors_address.send_keys('123 jolby street, jolbyville')

		# he is invited to add a tax type and rate
		tax_type = self.browser.find_element_by_id('new_tax_type_input')
		tax_type.send_keys('AST')

		tax_rate = self.browser.find_element_by_id('new_tax_rate_input')
		tax_rate.send_keys('25')

		# he then enter currency details
		currency_symbol = self.browser.find_element_by_id('new_currency_symbol_input')
		currency_symbol.send_keys('$')
		currency_name = self.browser.find_element_by_id('new_currency_name_input')
		currency_name.send_keys('CAD')

		# he is invited to add a line item, description, price and quantity
		line_item_input = self.browser.find_element_by_id('new_line_item_input')
		line_item_input.send_keys('Item #1')
		line_item_description_input = self.browser.find_element_by_id('new_line_item_description_input')
		line_item_description_input.send_keys('Description for Item #1')
		line_item_quantity_input = self.browser.find_element_by_id('new_line_item_quantity_input')
		line_item_quantity_input.send_keys('2')
		line_item_price_input = self.browser.find_element_by_id('new_line_item_price_input')
		line_item_price_input.send_keys('25')

		line_item_input.send_keys(Keys.ENTER)

		# After hitting enter he notices the page updates showing the entered values
		# and new inputs for another line item
		jolby_invoice_url = self.browser.current_url
		self.assertRegex(jolby_invoice_url, '/invoices/.+')

		invoice_number = self.browser.find_element_by_id('new_invoice_number_input')
		self.assertIn(invoice_number.get_attribute('value'), '1234')

		customer_address = self.browser.find_element_by_id('new_invoiced_customer_address_input')
		self.assertIn('123 street name, anytown', customer_address.get_attribute('value'))

		vendors_name = self.browser.find_element_by_id('new_vendors_name_input')
		self.assertIn('Jolby', vendors_name.get_attribute('value'))

		vendors_address = self.browser.find_element_by_id('new_vendors_address_input')
		self.assertIn('123 jolby street, jolbyville', vendors_address.get_attribute('value'))

		tax_type = self.browser.find_element_by_id('new_tax_type_input')
		self.assertIn('AST', tax_type.get_attribute('value'))

		tax_rate = self.browser.find_element_by_id('new_tax_rate_input')
		self.assertIn('25', tax_rate.get_attribute('value'))

		self.check_for_row_in_invoice_table('Line 1: Item #1')

		# He sees that he can add another line item and does so
		line_item_input = self.browser.find_element_by_id('new_line_item_input')
		line_item_input.send_keys('Item #2')
		line_item_description_input = self.browser.find_element_by_id('new_line_item_description_input')
		line_item_description_input.send_keys('Description for Item #2')
		line_item_quantity_input = self.browser.find_element_by_id('new_line_item_quantity_input')
		line_item_quantity_input.send_keys('1')

		line_item_input.send_keys(Keys.ENTER)

		# after the page refreshes both items are now visible
		self.check_for_row_in_invoice_table('Line 1: Item #1')
		self.check_for_row_in_invoice_table('Line 2: Item #2')

		# The invoice details are stil visible

		invoice_number = self.browser.find_element_by_id('new_invoice_number_input')
		self.assertIn('1234', invoice_number.get_attribute('value'))

		customer_address = self.browser.find_element_by_id('new_invoiced_customer_address_input')
		self.assertIn('123 street name, anytown', customer_address.get_attribute('value'))

		vendors_name = self.browser.find_element_by_id('new_vendors_name_input')
		self.assertIn('Jolby', vendors_name.get_attribute('value'))

		vendors_address = self.browser.find_element_by_id('new_vendors_address_input')
		self.assertIn('123 jolby street, jolbyville', vendors_address.get_attribute('value'))

		tax_type = self.browser.find_element_by_id('new_tax_type_input')
		self.assertIn('AST', tax_type.get_attribute('value'))

		tax_rate = self.browser.find_element_by_id('new_tax_rate_input')
		self.assertIn('25', tax_rate.get_attribute('value'))

		# A new user, Francis visits the site

		## new browser session to make sure no information 
		## from Jolby is coming through cookies etc.
		self.browser.quit()
		self.browser = webdriver.Firefox()

		# Francis visits the home page. There's no sign of Jolby's list
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Jolby', page_text)
		self.assertNotIn('Line 1: Item #1', page_text)
		self.assertNotIn('Line 2: Item #2', page_text)

		# Francis starts a new invoice 
		# he is invited to enter an invoice number
		invoice_number = self.browser.find_element_by_id('new_invoice_number_input')
		invoice_number.send_keys('4321')

		# he is invited to enter a customer and their address
		customer_name = self.browser.find_element_by_id('new_invoiced_customer_name_input')
		customer_name.send_keys('Mrs Customer')

		customer_address = self.browser.find_element_by_id('new_invoiced_customer_address_input')
		customer_address.send_keys('123 street name, anytown')

		# he is invited to enter his own name and address
		vendors_name = self.browser.find_element_by_id('new_vendors_name_input')
		vendors_name.send_keys('Francis')

		vendors_address = self.browser.find_element_by_id('new_vendors_address_input')
		vendors_address.send_keys('123 francis street, france')

		# he is invited to add a tax type and rate
		tax_type = self.browser.find_element_by_id('new_tax_type_input')
		tax_type.send_keys('AST')

		tax_rate = self.browser.find_element_by_id('new_tax_rate_input')
		tax_rate.send_keys('25')
		
		# he then enter currency details
		currency_symbol = self.browser.find_element_by_id('new_currency_symbol_input')
		currency_symbol.send_keys('$')
		currency_name = self.browser.find_element_by_id('new_currency_name_input')
		currency_name.send_keys('CAD')

		# he enters a new line item
		line_item_input = self.browser.find_element_by_id('new_line_item_input')
		line_item_input.send_keys('Francis Item #1')
		line_item_description_input = self.browser.find_element_by_id('new_line_item_description_input')
		line_item_description_input.send_keys('Description for Francis Item #2')
		line_item_quantity_input = self.browser.find_element_by_id('new_line_item_quantity_input')
		line_item_quantity_input.send_keys('1')

		line_item_quantity_input.send_keys(Keys.ENTER)

		# Francis gets his own unique URL
		francis_invoice_url = self.browser.current_url
		self.assertRegex(francis_invoice_url, '/invoices/.+')
		self.assertNotEqual(francis_invoice_url, jolby_invoice_url)

		# again, no trace of Jolby's invoice
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Jolby', page_text)
		self.assertNotIn('Line 1: Item #1', page_text)
		self.assertIn('Line 1: Francis Item #1', page_text)

		# he notices that some fields on the invoice are incorrect and so edits them
		tax_type = self.browser.find_element_by_id('new_tax_type_input')
		tax_type.send_keys('TAX')
		currency_name = self.browser.find_element_by_id('new_currency_name_input')
		currency_name.send_keys('USD\n')

		# when page refreshes he noticres that these fields have been updated
		tax_value = self.browser.find_element_by_id('new_tax_type_input').get_attribute('value')
		currency_value = self.browser.find_element_by_id('new_currency_name_input').get_attribute('value')
		self.assertIn('TAX', tax_value)
		self.assertIn('USD', currency_value)
		
		# he notices that after each line item is added the net, tax and total 
		# payable amounts increase by the correct amount


		# he notices that he can click a button to save the invoice as a pdf 


		# he notices that he can enter the customer's email address and send the 
		# invoice directly to them.
