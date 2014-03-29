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
		self.assertEqual('Create New Invoice', header_text)

		# he is invited to enter an invoice number
		invoice_number = self.browser.find_element_by_id('invoice_number_input')
		invoice_number.send_keys('1234')

		# he is prompted to enter tax and currency details
		currency_name = self.browser.find_element_by_id('currency_name_input')
		currency_name.send_keys('USD')
		currency_symbol = self.browser.find_elements_by_id('currency_symbol_input')
		currency_symbol.send_keys('$')

		tax_name = self.browser.find_element_by_id('tax_name_input')
		tax_name.send_keys('TST')
		tax_rate = self.browser.find_element_by_id('tax_rate_input')
		tax_rate.send_keys('15')

		# and any comments (like payment details or terms)
		invoice_comments = self.browser.find_element_by_id('invoice_comments_input')
		invoice_comments.send_keys('Please pay cash money within 30 days')

		# he clicks the continue button to, well continue
		self.browser.find_element_by_tag('button').click()

		# he sees that this page is to enter his (vendor) details
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertEqual(header_text, 'Enter your details')

		# As this is his first visit no details are auto populated for him.
		# He has to fill out the whole form.
		vendor_name = self.browser.find_element_by_id('vendor_name_input')
		vendor_name.send_keys('JolbyTech')
		vendor_street_address = self.browser.find_element_by_id('vendor_street_address_input')
		vendor_street_address.send_keys('123 vendor street')
		vendor_city = self.browser.find_element_by_id('vendor_city_input')
		vendor_city.send_keys('Jolbyville')
		vendor_state = self.browser.find_element_by_id('vendor_state_input')
		vendor_state.send_keys('ON')
		vendor_post_code = self.browser.find_element_by_id('vendor_post_code_input')
		vendor_post_code.send_keys('1234')
		vendor_phone_number = self.browser.find_element_by_id('vendor_phone_number_input')
		vendor_phone_number.send_keys('1 123 123 1234')
		vendor_email_address = self.browser.find_element_by_id('vendor_email_address_input')
		vendor_email_address.send_keys('jolby@jolbytech.com')

		# checking his work and seeing it is good he clicks continue
		self.browser.find_element_by_tag_name('button').click()

		# The next page that loads asks him to enter his customer's details
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertEqual(header_text, "Enter your customer's details")

		# following this simple instruction he fills out the form
		customer_name = self.browser.find_element_by_id('customer_name_input')
		customer_name.send_keys('Mr Customer')
		customer_street_address = self.browser.find_element_by_id('customer_street_address_input')
		customer_street_address.send_keys('123 customer street')
		customer_city = self.browser.find_element_by_id('customer_city_input')
		customer_city.send_keys('Customerton')
		customer_state = self.browser.find_element_by_id('customer_state_input')
		customer_state.send_keys('ON')
		customer_post_code = self.browser.find_element_by_id('customer_post_code_input')
		customer_post_code.send_keys('1234')
		customer_phone_number = self.browser.find_element_by_id('customer_phone_number_input')
		customer_phone_number.send_keys('1 123 123 1234')
		customer_email_address = self.browser.find_element_by_id('vendor_email_address_input')
		customer_email_address.send_keys('customer@email.com')

		# with that complete he clicks on continue
		self.browser.find_element_by_tag_name('button').click()

		# Jolby now sees all the data he's entered shown on the invoice
		invoice_number = self.browser.find_element_by_id('invoice_number').text
		self.assertEqual(invoice_number, '1234')
		invoice_comments = self.browser.find_element_by_id('invoice_comments').text
		self.assertEqual(invoice_comments, 'Please pay cash money within 30 days')
		
		customer_name = self.browser.find_element_by_id('customer_name').text
		self.assertEqual(customer_name, 'Mr Customer')
		customer_city = self.browser.find_element_by_id('customer_city').text
		self.assertEqual(customer_city, 'Customerton')
		customer_email = self.browser.find_element_by_id('customer_email').text
		self.assertEqual(customer_email, 'customer@email.com')

		vendor_name = self.browser.find_element_by_id('vendor_name').text
		self.assertEqual(vendor_name, 'JolbyTech')
		vendor_state = self.browser.find_element_by_id('vendor_state').text
		self.assertEqual(vendor_state, 'ON')
		vendor_phone_number = self.browser.find_element_by_id('vendor_phone_number').text
		self.assertEqual(vendor_phone_number, '1 123 123 1234')

		# This quick check satisfies that the details are as he entered them.
		# He also notices a link to edit vendor details and another to edit 
		# customer details. 
		edit_customer_link = self.browser.find_element_by_link_text('Edit customer details').text
		self.assertEqual(edit_customer_link, 'Edit customer details')

		edit_vendor_link = self.browser.find_element_by_link_text('Edit your details').text
		self.assertEqual(edit_vendor_link, 'Edit your details')
		
		# Jolby now sees an area to enter line items.
		# he is invited to add a line item, description, price and quantity
		line_item_input = self.browser.find_element_by_id('new_line_item_input')
		line_item_input.send_keys('Item #1')
		line_item_description_input = self.browser.find_element_by_id('new_line_item_description_input')
		line_item_description_input.send_keys('Description for Item #1')
		line_item_quantity_input = self.browser.find_element_by_id('new_line_item_quantity_input')
		line_item_quantity_input.send_keys('1')
		line_item_price_input = self.browser.find_element_by_id('new_line_item_price_input')
		line_item_price_input.send_keys('100')

		# He clicks the Add button to save the line item to the invoice
		self.browser.find_element_by_tag_name('button').click()

		# After hitting enter he notices the page updates showing the entered values
		# and new inputs for another line item. His invoice details remain unchanged.

		invoice_number = self.browser.find_element_by_id('invoice_number').text
		self.assertEqual(invoice_number, '1234')

		vendor_name = self.browser.find_element_by_id('vendor_name')
		self.assertEqual(vendor_name, 'JolbyTech')

		# He enters details for his another line item 
		line_item_input = self.browser.find_element_by_id('line_item_input')
		line_item_input.send_keys('Item #2')
		line_item_description_input = self.browser.find_element_by_id('line_item_description_input')
		line_item_description_input.send_keys('Description for Item #2')
		line_item_quantity_input = self.browser.find_element_by_id('line_item_quantity_input')
		line_item_quantity_input.send_keys('2')

		line_item_price_input = self.browser.find_element_by_id('line_item_price_input')
		line_item_price_input.send_keys('200')

		# He clicks the Add button again
		self.browser.find_element_by_tag_name('button').click()

		# after the page refreshes both items are now visible
		self.check_for_row_in_invoice_table('Line 1: Item #1')
		self.check_for_row_in_invoice_table('Line 2: Item #2')

		# He notices a link that he can click to delete a line item


		# He decides to try it out by clicking the delete link next to Item 2



		# A new user, Francis visits the site

		## new browser session to make sure no information 
		## from Jolby is coming through cookies etc.
		self.browser.quit()
		self.browser = webdriver.Firefox()

		# Francis visits the home page. There's no sign of Jolby's invoice 
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Jolby', page_text)
		self.assertNotIn('1234', page_text)
		self.assertNotIn('Please pay cash money within 30 days', page_text)

		# Francis starts a new invoice 
		# he is invited to enter an invoice number
		invoice_number = self.browser.find_element_by_id('invoice_number_input')
		invoice_number.send_keys('4321')


		# He sees a link to download the invoice as a pdf

		# he notices that he can send the invoice directly to the 
		# customer using address provided earlier
