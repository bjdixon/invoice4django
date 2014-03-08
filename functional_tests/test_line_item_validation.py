from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class LineItemValidationTest(FunctionalTest):

	def test_cannot_add_empty_line_item(self):
		# jolby goes to the home page and accidentally tries
		# to submit an empty line item. hits enter on empty input
		self.browser.get(self.live_server_url)
		self.browser.find_element_by_id('new_line_item_quantity_input').send_keys('\n')

		error = self.browser.find_element_by_css_selector('.has-error')
		self.assertEqual(error.text, "You can't have an empty line item")

		# he tries to add a new item
		self.browser.find('new_line_item_input').send_keys('Item 1')
		self.browser.find('new_line_item_description_input').send_keys('Description 1')
		self.browser.find('new_line_item_quantity_input').send_keys('2\n')

		self.check_for_row_in_invoice_table('Item 1')

		# just to see he tries to enter another empty line item
		self.browser.find_element_by_id('new_line_item_quantity_input').send_keys('\n')

		# he receives a similar warning
		self.check_for_row_in_invoice_table('Item 1')
		error = self.browser.find_element_by_css_selector('.has-error')
		self.assertEqual(error.text, "You can't have an empty line item")


