from django import forms

class PaymentForm(forms.Form):
    PAYMENT_CHOICES = [
        ('credit', 'Credit Card'),
        ('transfer', 'Bank Transfer'),
        ('loan', 'Loan')
    ]

    payment_method = forms.CharField(required=True)

    card_carrier = forms.CharField(required=False)
    card_number = forms.CharField(required=False)
    expiry_date = forms.CharField(required=False)
    cvv = forms.CharField(required=False)

    bank_number = forms.CharField(required=False)

    lender = forms.CharField(required=False)