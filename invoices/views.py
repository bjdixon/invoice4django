from django.shortcuts import render, redirect
from django.http import HttpResponse

from invoices.models import Invoice, Line_item

# Create your views here.
def home_page(request):
	return render(request, 'home.html')

def view_invoice(request):
	line_items = Line_item.objects.all()
	return render(request, 'invoice.html', {'line_items': line_items})

def new_invoice(request):
	invoice_ = Invoice.objects.create()
	Line_item.objects.create(
		line_item=request.POST['line_item'],
		line_item_description=request.POST['line_item_description'],
		line_item_quantity=request.POST['line_item_quantity'],
		invoice = invoice_
	)
	return redirect('/invoices/the-only-invoice-in-the-world/')

