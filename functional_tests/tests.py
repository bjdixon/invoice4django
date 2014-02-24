from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def check_for_row_in_invoice_table(self, row_text):
		table = self.browser.find_element_by_id('invoice_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

	def test_can_start_an_invoice_and_retrieve_it_later(self):
		# Jolby has heard about a new invoice site. He goes
		# to check out it's home page.
		self.browser.get(self.live_server_url)

		# he notices the page title and header mention Invoices
		self.assertIn('Invoices', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('Invoices', header_text)

		# he is invited to enter an invoice number


		# he is invited to enter a customer and their address


		# he is invited to enter his own name and address


		# he is invited to add a tax type and tax percentage


		# he is invited to add a line item, description, price and quantity
		line_item_input = self.browser.find_element_by_id('new_line_item_input')
		line_item_input.send_keys('Item #1')
		line_item_description_input = self.browser.find_element_by_id('new_line_item_description_input')
		line_item_description_input.send_keys('Description for Item #1')
		line_item_quantity_input = self.browser.find_element_by_id('new_line_item_quantity_input')
		line_item_quantity_input.send_keys('2')

		line_item_input.send_keys(Keys.ENTER)

		# After hitting enter he notices the page updates showing the entered values
		# and new inputs for another line item
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

		


		# he notices that after each line item is added the net, tax and total 
		# payable amounts increase by the correct amount


		# he notices that he can click a button to save the invoice as a pdf 


		# he notices that he can enter the customer's email address and send the 
		# invoice directly to them.


		self.fail('finish the test')


