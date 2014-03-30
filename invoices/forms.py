from django import forms
from django.core.exceptions import ValidationError

from invoices.models import Invoice, Currency, Tax, Vendor, Customer, Line_item

EMPTY_NAME_ERROR = 'The name for a company or individual is needed'
EMPTY_STREET_ADDRESS_ERROR = 'A street address is required'
EMPTY_CITY_ERROR = 'Please include the city'
EMPTY_STATE_ERROR = 'A state or province is required'
EMPTY_POST_CODE_ERROR = 'You forgot the post code'
EMPTY_PHONE_NUMBER_ERROR = 'Please put your phone number in'
EMPTY_EMAIL_ADDRESS_ERROR = 'You still need to enter a valid email address'
EMPTY_INVOICE_NUMBER_ERROR = 'This field is required.'
EMPTY_LINE_ITEM_ERROR = 'You need to enter a line item'
EMPTY_LINE_ITEM_QUANTITY_ERROR = 'Please enter a quantity'
EMPTY_LINE_ITEM_PRICE_ERROR = "You didn't enter a price"


class InvoiceForm(forms.models.ModelForm):

	class Meta:
		model = Invoice
		fields = ('invoice_number', 'invoice_date', 'invoice_comment')
		widgets = {
				'invoice_number': forms.fields.TextInput(attrs={
					'placeholder': 'Enter an invoice number',
					'class': 'form-control input-lg',
				}),
				'invoice_date': forms.fields.DateInput(attrs={
					'placeholder': 'Enter date',
					'class': 'form-control input-lg',
				}),
				'invoice_comment': forms.fields.TextInput(attrs={
					'placeholder': 'Enter any comments, like terms and conditions',
					'class': 'form-control input-lg',
				}),
		}

		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.fields['invoice_number'].error_messages['required'] = EMPTY_INVOICE_NUMBER_ERROR 


class CurrencyForm(forms.models.ModelForm):

	class Meta:
		model = Currency
		fields = ('currency_name', 'currency_symbol')
		widgets = {
				'currency_name': forms.fields.TextInput(attrs={
					'placeholder': 'Enter a currency name',
					'class': 'form-control input-lg',
				}),
				'currency_symbol': forms.fields.TextInput(attrs={
					'placeholder': 'Enter the symbol for this currency',
					'class': 'form-field input-lg',
				}),
		}


	def save(self, invoice):
		self.instance.invoice = invoice
		return super().save()


class TaxForm(forms.models.ModelForm):

	class Meta:
		model = Tax
		fields = ('tax_name', 'tax_rate')
		widgets = {
				'tax_name': forms.fields.TextInput(attrs={
					'placeholder':	'Enter a tax type',
					'class': 'form-control input-lg',
				}),
				'tax_rate': forms.fields.TextInput(attrs={
					'placeholder': 'Enter the tax rate',
					'class': 'form-control input-lg',
				}),
		}

	def save(self, invoice):
		self.instance.invoice = invoice
		return super().save()


class VendorForm(forms.models.ModelForm):

	class Meta:
		model = Vendor
		fields = (
				'vendor_name', 'vendor_street_address', 'vendor_city', 'vendor_state',
				'vendor_post_code', 'vendor_phone_number', 'vendor_email_address'
				)
		widgets = {
				'vendor_name': forms.fields.TextInput(attrs={
					'placeholder': 'Enter your company name',
					'class': 'form-control input-lg',
				}),
				'vendor_street_address': forms.fields.TextInput(attrs={
					'placeholder': 'Enter your street address',
					'class': 'form-control input-lg',
				}),
				'vendor_city': forms.fields.TextInput(attrs={
					'placeholder': 'Enter your city',
					'class': 'form-control input-lg',
				}),
				'vendor_state': forms.fields.TextInput(attrs={
					'placeholder': 'Enter your state',
					'class': 'form-control input-lg',
				}),
				'vendor_post_code': forms.fields.TextInput(attrs={
					'placeholder': 'Enter your postal code',
					'class': 'form-control input-lg',
				}),
				'vendor_phone_number': forms.fields.TextInput(attrs={
					'placeholder': 'Enter your phone number',
					'class': 'form-control input-lg',
				}),
				'vendor_email_address': forms.fields.EmailInput(attrs={
					'placeholder': 'Enter your email address',
					'class': 'form-control input-lg',
				}),
			}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['vendor_name'].error_messages['required'] = EMPTY_NAME_ERROR
		self.fields['vendor_street_address'].error_messages['required'] = EMPTY_STREET_ADDRESS_ERROR
		self.fields['vendor_city'].error_messages['required'] = EMPTY_CITY_ERROR
		self.fields['vendor_state'].error_messages['required'] = EMPTY_STATE_ERROR
		self.fields['vendor_post_code'].error_messages['required'] = EMPTY_POST_CODE_ERROR
		self.fields['vendor_phone_number'].error_messages['required'] = EMPTY_PHONE_NUMBER_ERROR
		self.fields['vendor_email_address'].error_messages['required'] = EMPTY_EMAIL_ADDRESS_ERROR
		self.fields['vendor_email_address'].error_messages['invalid'] = EMPTY_EMAIL_ADDRESS_ERROR

	def save(self, invoice):
		self.instance.invoice = invoice
		return super().save()


class CustomerForm(forms.models.ModelForm):

	class Meta:
		model = Customer
		fields = (
				'customer_name', 'customer_street_address', 'customer_city', 'customer_state',
				'customer_post_code', 'customer_phone_number', 'customer_email_address'
				)
		widgets = {
				'customer_name': forms.fields.TextInput(attrs={
					'placeholder': 'Enter customer company name',
					'class': 'form-control input-lg',
				}),
				'customer_street_address': forms.fields.TextInput(attrs={
					'placeholder': 'Enter customer street address',
					'class': 'form-control input-lg',
				}),
				'customer_city': forms.fields.TextInput(attrs={
					'placeholder': 'Enter customer city',
					'class': 'form-control input-lg',
				}),
				'customer_state': forms.fields.TextInput(attrs={
					'placeholder': 'Enter customer state',
					'class': 'form-control input-lg',
				}),
				'customer_post_code': forms.fields.TextInput(attrs={
					'placeholder': 'Enter customer postal code',
					'class': 'form-control input-lg',
				}),
				'customer_phone_number': forms.fields.TextInput(attrs={
					'placeholder': 'Enter customer phone number',
					'class': 'form-control input-lg',
				}),
				'customer_email_address': forms.fields.EmailInput(attrs={
					'placeholder': 'Enter customer email address',
					'class': 'form-control input-lg',
				}),
			}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['customer_name'].error_messages['required'] = EMPTY_NAME_ERROR
		self.fields['customer_street_address'].error_messages['required'] = EMPTY_STREET_ADDRESS_ERROR
		self.fields['customer_city'].error_messages['required'] = EMPTY_CITY_ERROR
		self.fields['customer_state'].error_messages['required'] = EMPTY_STATE_ERROR
		self.fields['customer_post_code'].error_messages['required'] = EMPTY_POST_CODE_ERROR
		self.fields['customer_phone_number'].error_messages['required'] = EMPTY_PHONE_NUMBER_ERROR
		self.fields['customer_email_address'].error_messages['required'] = EMPTY_EMAIL_ADDRESS_ERROR
		self.fields['customer_email_address'].error_messages['invalid'] = EMPTY_EMAIL_ADDRESS_ERROR

	def save(self, invoice):
		self.instance.invoice = invoice
		return super().save()


class LineItemForm(forms.models.ModelForm):

	class Meta:
		model = Line_item
		fields = (
				'line_item', 'line_item_description', 
				'line_item_quantity', 'line_item_price'
				)
		widgets = {
				'line_item': forms.fields.TextInput(attrs={
					'placeholder': 'Enter a line item',
					'class': 'form-control input-lg',
				}),
				'line_item_description': forms.fields.TextInput(attrs={
					'placeholder': 'Enter a description',
					'class': 'form-control input-lg',
				}),
				'line_item_quantity': forms.fields.TextInput(attrs={
					'placeholder': 'Enter the quantity',
					'class': 'form-control input-lg',
				}),
				'line_item_price': forms.fields.TextInput(attrs={
					'placeholder': 'Enter the price per item',
					'class': 'form-control input-lg',
				}),
			}

	
				
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['line_item'].error_messages['required'] = EMPTY_LINE_ITEM_ERROR
		self.fields['line_item_quantity'].error_messages['required'] = EMPTY_LINE_ITEM_QUANTITY_ERROR
		self.fields['line_item_price'].error_messages['required'] = EMPTY_LINE_ITEM_PRICE_ERROR

	def save(self, invoice):
		self.instance.invoice = invoice
		return super().save()


