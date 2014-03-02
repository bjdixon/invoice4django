from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'invoice4django.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	#url(r'^admin/', include(admin.site.urls)),
	url(r'^$', 'invoices.views.home_page', name='home'),
	url(r'^invoices/the-only-invoice-in-the-world/$', 'invoices.views.view_invoice', name='view_invoice'),
)
