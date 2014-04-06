from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError

from invoices.forms import *
from invoices.models import *


def home_page(request):
	invoice_form = InvoiceForm(request.POST or None)
	currency_form = CurrencyForm(request.POST or None)
	tax_form = TaxForm(request.POST or None)
	if invoice_form.is_valid() and currency_form.is_valid() and tax_form.is_valid():
		invoice_ = invoice_form.save()
		currency_form.save(invoice=invoice_)
		tax_form.save(invoice=invoice_)
		return redirect('/invoices/%d/vendor/' % (invoice_.id,))
	else:
		return render(request, 'home.html', {
			'invoice_form': InvoiceForm(),
			'currency_form': CurrencyForm(),
			'tax_form': TaxForm(),
		})

def vendor_page(request, invoice):
	invoice_ = Invoice.objects.get(id=invoice)
	form = VendorForm(request.POST or None)
	if form.is_valid():
		form.save(invoice=invoice_)
		return redirect('/invoices/%d/customer/' % (invoice_.id,))
	else:
		return render(request, 'vendor.html', {'form': VendorForm(),})	

def customer_page(request, invoice):
	invoice_ = Invoice.objects.get(id=invoice)
	form = CustomerForm(request.POST or None)
	if form.is_valid():
		form.save(invoice=invoice_)
		return redirect('/invoices/%d/line_item/' % (invoice_.id,))
	else:
		return render(request, 'customer.html', {'form': CustomerForm(),})	

def line_item_page(request, invoice):
	invoice_ = Invoice.objects.get(id=invoice)
	form = LineItemForm(request.POST or None)
	if form.is_valid():
		form.save(invoice=invoice_)
		return redirect('/invoices/%d/line_item/' % (invoice_.id,))
	else:
		line_items = Line_item.objects.filter(invoice=invoice_)
		vendor = Vendor.objects.get(invoice=invoice_)
		customer = Customer.objects.get(invoice=invoice_)
		currency = Currency.objects.get(invoice=invoice_)
		tax = Tax.objects.get(invoice=invoice_)
		return render(request, 'line_item.html', {
			'form': LineItemForm(),
			'invoice': invoice_,
			'vendor': vendor,
			'customer': customer,
			'currency': currency,
			'tax': tax,
			'line_items': line_items,
		})	

