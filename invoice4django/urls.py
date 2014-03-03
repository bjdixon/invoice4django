from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'invoice4django.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	#url(r'^admin/', include(admin.site.urls)),
	url(r'^$', 'invoices.views.home_page', name='home'),
	url(r'^invoices/(\d+)/$', 'invoices.views.view_invoice', name='view_invoice'),
	url(r'^invoices/(\d+)/new_item$', 'invoices.views.add_item', name='add_item'),
	url(r'^invoices/new$', 'invoices.views.new_invoice', name='new_invoice'),
)
