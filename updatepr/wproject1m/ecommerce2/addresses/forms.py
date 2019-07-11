from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            # 'billing_profile',
            # 'address_type',
            'address_line_1',
            'address_line_2',
            'city',
            'country',
            # 'state',
            'postal_code',
        ]





