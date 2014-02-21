from django.shortcuts import render
from django.http import HttpResponse

from invoices.models import Invoice, Line_item

# Create your views here.
def home_page(request):
	invoice = Invoice()
	invoice.invoice_number = request.POST.get('invoice_number', '')
	invoice.invoiced_customer_name = request.POST.get('invoiced_customer_name', '')
	invoice.invoiced_customer_address = request.POST.get('invoiced_customer_address', '')
	invoice.vendors_name = request.POST.get('vendors_name', '')
	invoice.vendors_address = request.POST.get('vendors_address', '')
	invoice.tax_type = request.POST.get('tax_type', '')
	invoice.tax_rate = request.POST.get('tax_rate', '')
	invoice.save()
	return render(request, 'home.html', {
		'invoice_number_output': invoice.invoice_number,
		'invoiced_customer_name_output': invoice.invoiced_customer_name,
		'invoiced_customer_address_output': invoice.invoiced_customer_address,
		'vendors_name_output': invoice.vendors_name,
		'vendors_address_output': invoice.vendors_address,
		'tax_type_output': invoice.tax_type,
		'tax_rate_output': invoice.tax_rate,
	})

