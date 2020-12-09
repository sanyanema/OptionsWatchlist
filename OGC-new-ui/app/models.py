
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Transaction(models.Model):
    # transaction_ID = models.IntegerField()
    # expiration date, ticker. I can maybe get rid of stock ticker field.
    expiration_date = models.CharField(default="",max_length=200)
    contract_symbol = models.CharField(default="",max_length=200)
    purchase_price = models.IntegerField(default=-999)
    quantity = models.IntegerField(default=100)
    closed = models.BooleanField(default=False)
    typ = models.CharField(default="",max_length=200)
    strike = models.IntegerField(default=-999)

    def __str__(self):
        return self.contract_symbol
class Account(models.Model):
    user_id = models.CharField(max_length=200,unique=True,null=True)
    balance = models.IntegerField(default=1000000)
    transaction = models.ManyToManyField(Transaction, related_name="transaction", null=True, blank=True)
    watchlist = models.TextField(default="", blank=True)
    # needs fixes

    def __str__(self):
        return self.user_id

