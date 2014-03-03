from django.shortcuts import render, redirect
from django.http import HttpResponse

from invoices.models import Invoice, Line_item

# Create your views here.
def home_page(request):
	return render(request, 'home.html')

def view_invoice(request, invoice_id):
	invoice_ = Invoice.objects.get(id=invoice_id)
	items = Line_item.objects.filter(invoice=invoice_)
	return render(request, 'invoice.html', {'invoice': invoice_, 'items': items})

def new_invoice(request):
	invoice_ = Invoice.objects.create()
	Line_item.objects.create(
		line_item=request.POST['line_item'],
		line_item_description=request.POST['line_item_description'],
		line_item_quantity=request.POST['line_item_quantity'],
		invoice=invoice_
	)
	return redirect('/invoices/%d/' % (invoice_.id,))

def add_item(request, invoice_id):
	invoice_ = Invoice.objects.get(id=invoice_id)
	Line_item.objects.create(
		line_item=request.POST['line_item'],
		line_item_description=request.POST['line_item_description'],
		line_item_quantity=request.POST['line_item_quantity'],
		invoice=invoice_
	)
	return redirect('/invoices/%d/' % (invoice_.id,))

