from django.db import models

# Create your models here.
class Payments(models.Model):
    class PaymentMethod(models.TextChoices):
        CREDIT_CARD = 'creditcard', 'Credit Card'
        TRANSFER = 'transfer', 'Bank Transfer'
        LOAN = 'loan', 'Loan'

    offer = models.ForeignKey('offer.Offers', on_delete=models.CASCADE)
    amount = models.IntegerField()
    time = models.DateTimeField()
    method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CREDIT_CARD,
    )