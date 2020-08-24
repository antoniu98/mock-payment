from django import forms
from gateways.validators import credit_card_validator, expiration_date_validator, security_code_validator, amount_validator

""" 
The idea behind this form implementation was NOT to duplicate/reuse code, but rather to keep the idea that on both sides, Checkout
or Gateway services, the form MUST have a validation before being sent out, maybe the validation is different, but in this case 
I kept the same validation rules for both services. This is the reason why I imported from gateway service
"""

class PaymentForm(forms.Form):
    credit_card_number = forms.CharField(required=True, validators=[credit_card_validator], max_length = 20)
    card_holder = forms.CharField(required=True, max_length = 30)
    expiration_date = forms.DateTimeField(required=True, validators=[expiration_date_validator], input_formats=['%Y-%m'],\
                        widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM'}))
    security_code = forms.CharField(validators=[security_code_validator], max_length = 3)
    amount = forms.DecimalField(required=True, validators=[amount_validator], max_digits=9, decimal_places=2)
