from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError

from invoices.forms import *
from invoices.models import *

# Create your views here.
def home_page(request):
	return render(request, 'home.html', {
		'invoice_form': InvoiceForm(),
		'currency_form': CurrencyForm(),
		'tax_form': TaxForm(),
	})

def vendor_page(request, invoice):
	form = VendorForm(data=request.POST)
	if form.is_valid():
		form.save(invoice=invoice)
		return redirect(invoice)
	else:
		return render(request, 'vendor.html', {'form': form})	

def customer_page(request, invoice):
	return render(request, 'customer.html')	

def line_item_page(request, invoice):
	return render(request, 'line_item.html')	

