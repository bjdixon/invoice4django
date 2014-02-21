from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_page(request):
	return render(request, 'home.html', {
		'invoice_number_output': request.POST.get('invoice_number', ''),
		'invoiced_customer_name_output': request.POST.get('invoiced_customer_name', ''),
		'invoiced_customer_address_output': request.POST.get('invoiced_customer_address', ''),
		'vendors_name_output': request.POST.get('vendors_name', ''),
		'vendors_address_output': request.POST.get('vendors_address', ''),
		'tax_type_output': request.POST.get('tax_type', ''),
		'tax_rate_output': request.POST.get('tax_rate', ''),
	})

