from django.core.exceptions import ValidationError
from datetime import datetime

def credit_card_validator(card):
    if not card.isdigit() or len(card) != 16:
        raise ValidationError(
            ('%(card)s is not a valid credit card number.'),
            params={'card': card},
        )

def expiration_date_validator(exp_date):
    if exp_date.date() <=  datetime.now().date():
        raise ValidationError(
            ('%(exp_date)s is not a valid expiration date or the card expired.'),
            params={'exp_date': exp_date},
        )

def security_code_validator(code):
    if not code.isdigit() or len(code) != 3:
        raise ValidationError(
            ('%(code)s is not a valid security code.'),
            params={'code': code},
        )

def amount_validator(amount):
    if amount <= 0:
        raise ValidationError(
            ('%(amount)s must be positive.'),
            params={'amount': amount},
        )