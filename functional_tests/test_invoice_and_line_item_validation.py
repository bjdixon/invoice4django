from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class InvoiceValidationTest(FunctionalTest):

	def test_cannot_add_invoice(self):
		# jolby goes to the home page and accidentally tries
		# to submit an empty line item. hits enter on empty input
		self.browser.get(self.live_server_url)
		self.browser.find_element_by_id('line_item_quantity_input').send_keys('\n')

		error = self.browser.find_element_by_css_selector('.has-error')
		self.assertEqual(error.text, "You can't save an empty invoice")
