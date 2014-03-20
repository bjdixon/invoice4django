from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError

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
	try: 
		invoice_ = Invoice.objects.create(
			invoice_number = request.POST['invoice_number'],
			invoiced_customer_name = request.POST['invoiced_customer_name'],
			invoiced_customer_address = request.POST['invoiced_customer_address'],
			vendors_name = request.POST['vendors_name'],
			vendors_address = request.POST['vendors_address'],
			tax_type = request.POST['tax_type'],
			tax_rate = request.POST['tax_rate']
		)
	except ValidationError:
		error_text = "You can't save an empty invoice"
		return render(request, 'home.html', {"error": error_text})	
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
	invoice_.invoice_number = request.POST['invoice_number'] or invoice_.invoice_number
	invoice_.invoiced_customer_name = request.POST['invoiced_customer_name'] or invoice_.invoiced_customer_name
	invoice_.invoiced_customer_address = request.POST['invoiced_customer_address'] or invoice_.invoiced_customer_address
	invoice_.tax_type = request.POST['tax_type'] or invoice_.tax_type
	invoice_.tax_rate = request.POST['tax_rate'] or invoice_.tax_rate
	invoice_.save()
	currency_ = Currency.objects.filter(invoice=invoice_).first() or Currency.objects.create(invoice=invoice_)
	currency_.currency_symbol = request.POST['currency_symbol'] or currency_.currency_symbol
	currency_.currency_name = request.POST['currency_name'] or currency_.currency_name
	currency_.save()
	Line_item.objects.create(
		line_item=request.POST.get('line_item', False), 
		line_item_description=request.POST.get('line_item_description', False),
		line_item_quantity=request.POST.get('line_item_quantity', False),
		line_item_price=request.POST.get('line_item_price', False),
		invoice=invoice_
	)
	return redirect('/invoices/%d/' % (invoice_.id,))

