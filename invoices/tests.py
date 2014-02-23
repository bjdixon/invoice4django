from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from invoices.views import home_page
from invoices.models import Invoice, Line_item

class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)

	def test_home_page_can_save_a_POST_request(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['line_item'] = 'Item #1'
		request.POST['line_item_description'] = 'Description of Item #1'
		request.POST['line_item_quantity'] = '2'

		response = home_page(request)
		
		self.assertEqual(Line_item.objects.all().count(), 1)
		new_line_item = Line_item.objects.all()[0]
		self.assertEqual(new_line_item.line_item, 'Item #1')

	def test_home_page_redirects_after_POST(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['line_item'] = 'Item #1'
		request.POST['line_item_description'] = 'Description of Item #1'
		request.POST['line_item_quantity'] = '2'

		response = home_page(request)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response['location'], '/')

	def test_home_page_only_saves_line_items_when_necessary(self):
		request = HttpRequest()
		home_page(request)
		self.assertEqual(Line_item.objects.all().count(), 0)

	def test_saving_and_retrieving_line_items(self):
		first_line_item = Line_item()
		first_line_item.line_item = 'Item #1'
		first_line_item.line_item_description = 'Description of Item #1'
		first_line_item.line_item_quantity = '2'
		first_line_item.save()

		second_line_item = Line_item()
		second_line_item.line_item = 'Item #2'
		second_line_item.line_item_description = 'Description of Item #2'
		second_line_item.line_item_quantity = '1'
		second_line_item.save()

		saved_line_items = Line_item.objects.all()
		self.assertEqual(saved_line_items.count(), 2)

		first_saved_line_item = saved_line_items[0]
		second_saved_line_item = saved_line_items[1]
		self.assertEqual(first_saved_line_item.line_item, first_line_item.line_item)
		self.assertEqual(second_saved_line_item.line_item_quantity, second_line_item.line_item_quantity)

