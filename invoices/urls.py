from django.conf.urls import patterns, include, url
from django.contrib import admin

from invoices import views

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', views.home_page, name='home_page'),
	url(r'^(\d+)/vendor/', views.vendor_page, name='vendor_page'),
	url(r'^(\d+)/customer/', views.customer_page, name='customer_page'),
	url(r'^(\d+)/line_item/', views.line_item_page, name='line_item_page'),
)
