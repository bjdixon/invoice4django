from django.shortcuts import render, redirect
from django.http import HttpResponse

from invoices.models import Invoice, Line_item, Currency

# Create your views here.
def home_page(request):
	return render(request, 'home.html')

def view_invoice(request, invoice_id):
	invoice_ = Invoice.objects.get(id=invoice_id)
	items = Line_item.objects.filter(invoice=invoice_)
	currency_ = Currency.objects.filter(invoice=invoice_).first()
	return render(request, 'invoice.html', {'invoice': invoice_, 'items': items, 'currency': currency_})

def new_invoice(request):
	invoice_ = Invoice.objects.create(
		invoice_number = request.POST['invoice_number'],
		invoiced_customer_name = request.POST['invoice_number'],
		invoiced_customer_address = request.POST['invoiced_customer_address'],
		vendors_name = request.POST['vendors_name'],
		vendors_address = request.POST['vendors_address'],
		tax_type = request.POST['tax_type'],
		tax_rate = request.POST['tax_rate']
	)
	Line_item.objects.create(
		line_item=request.POST['line_item'],
		line_item_description=request.POST['line_item_description'],
		line_item_quantity=request.POST['line_item_quantity'],
		line_item_price=request.POST['line_item_price'],
		invoice=invoice_
	)
	Currency.objects.create(
		currency_symbol=request.POST['currency_symbol'],
		currency_name=request.POST['currency_name'],
		invoice=invoice_
	)
	return redirect('/invoices/%d/' % (invoice_.id,))

def add_item(request, invoice_id):
	invoice_ = Invoice.objects.get(id=invoice_id)
	Line_item.objects.create(
		line_item=request.POST['line_item'],
		line_item_description=request.POST['line_item_description'],
		line_item_quantity=request.POST['line_item_quantity'],
		line_item_price=request.POST['line_item_price'],
		invoice=invoice_
	)
	return redirect('/invoices/%d/' % (invoice_.id,))

