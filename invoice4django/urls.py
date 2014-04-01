from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'invoices.views.home_page', name='home_page'),
	url(r'^invoices/', include('invoices.urls')),
)
