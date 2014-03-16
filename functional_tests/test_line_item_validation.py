from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class InvoiceValidationTest(FunctionalTest):

	def test_cannot_add_invoice(self):
		# jolby goes to the home page and accidentally tries
		# to submit an empty line item. hits enter on empty input
		self.browser.get(self.live_server_url)
		self.browser.find_element_by_id('new_line_item_quantity_input').send_keys('\n')

		error = self.browser.find_element_by_css_selector('.has-error')
		self.assertEqual(error.text, "All invoice details need to be filled out")

		# he adds invoice details
		invoice_number = self.browser.find_element_by_id('new_invoice_number_input')
		invoice_number.send_keys('1234')

		customer_name = self.browser.find_element_by_id('new_invoiced_customer_name_input')
		customer_name.send_keys('Mr Customer')

		customer_address = self.browser.find_element_by_id('new_invoiced_customer_address_input')
		customer_address.send_keys('123 street name, anytown')

		vendors_name = self.browser.find_element_by_id('new_vendors_name_input')
		vendors_name.send_keys('Jolby')

		vendors_address = self.browser.find_element_by_id('new_vendors_address_input')
		vendors_address.send_keys('123 jolby street, jolbyville')

		tax_type = self.browser.find_element_by_id('new_tax_type_input')
		tax_type.send_keys('AST')

		tax_rate = self.browser.find_element_by_id('new_tax_rate_input')
		tax_rate.send_keys('25')

		currency_symbol = self.browser.find_element_by_id('new_currency_symbol_input')
		currency_symbol.send_keys('$')
		currency_name = self.browser.find_element_by_id('new_currency_name_input')
		currency_name.send_keys('CAD')
		
		# he adds a line item
		self.browser.find('new_line_item_input').send_keys('Item 1')
		self.browser.find('new_line_item_description_input').send_keys('Description 1')
		self.browser.find('new_line_item_quantity_input').send_keys('2\n')

		self.check_for_row_in_invoice_table('Item 1')

		# just to see he tries to enter another empty line item
		self.browser.find_element_by_id('new_line_item_quantity_input').send_keys('\n')

		# nothing happens. nothing is updated and no error received
		self.check_for_row_in_invoice_table('Item 1')


