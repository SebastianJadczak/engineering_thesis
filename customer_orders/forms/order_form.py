from django import forms

from customer_orders.models import CustomerOrder


class OrderForm(forms.ModelForm):
    class Meta:
        model = CustomerOrder
        fields = ['zip_code', 'location', 'address', 'email', 'customer_last_name', 'customer_first_name']
