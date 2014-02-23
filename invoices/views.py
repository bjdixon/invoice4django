from django.shortcuts import render, redirect
from django.http import HttpResponse

from invoices.models import Invoice, Line_item

# Create your views here.
def home_page(request):
	if request.method == 'POST':
		Line_item.objects.create(
			line_item=request.POST['line_item'],
			line_item_description = request.POST['line_item_description'],
			line_item_quantity = request.POST['line_item_quantity']
		)
		return redirect('/')
			
	line_items = Line_item.objects.all()
	return render(request, 'home.html', {'line_items': line_items})
