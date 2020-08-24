from django.db import models
from .validators import credit_card_validator, expiration_date_validator, security_code_validator, amount_validator


# Create your models here.
class ProccessPaymentModel(models.Model):
    credit_card_number = models.CharField(validators=[credit_card_validator], max_length = 20)
    card_holder = models.CharField(max_length = 30)
    expiration_date = models.DateTimeField(validators=[expiration_date_validator])
    security_code = models.CharField(validators=[security_code_validator], max_length = 3)
    amount = models.DecimalField(validators=[amount_validator], max_digits=3, decimal_places=2)