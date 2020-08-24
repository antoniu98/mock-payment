from django import forms
from .models import ProccessPaymentModel
from .validators import credit_card_validator, expiration_date_validator, security_code_validator, amount_validator

class PaymentForm(forms.Form):
    credit_card_number = forms.CharField(required=True, validators=[credit_card_validator], max_length = 20)
    card_holder = forms.CharField(required=True, max_length = 30)
    expiration_date = forms.DateTimeField(required=True, validators=[expiration_date_validator])#, input_formats=['%Y-%m'])
    security_code = forms.CharField(validators=[security_code_validator], max_length = 3)
    amount = forms.DecimalField(required=True, validators=[amount_validator], max_digits=9, decimal_places=2)

    class Meta:
        model = ProccessPaymentModel
        fields = ['credit_card_number', 'card_holder', 'expiration_date', 'security_code', 'amount']