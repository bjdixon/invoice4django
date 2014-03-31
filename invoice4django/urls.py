from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'invoices.views.home_page', name='home'),
	url(r'^invoices/(\d+)/customer/', 'invoices.views.customer_page', name='customer'),
	url(r'^invoices/(\d+)/vendor/', 'invoices.views.vendor_page', name='vendor'),
	url(r'^invoices/(\d+)/line_item/', 'invoices.views.line_item_page', name='line_item'),
	url(r'^invoices/', include('invoices.urls')),
)
