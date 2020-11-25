# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Transaction(models.Model):
    transaction_ID = models.IntegerField()
    # expiration date, ticker. I can maybe get rid of stock ticker field.
    expiration_date = models.DateField()
    contract_symbol = models.CharField(default="",max_length=200,unique=True)
    stock = models.CharField(default="",max_length=200,unique=True)
    purchase_price = models.IntegerField(default=-999)
    quantity = models.IntegerField(default=100)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return self.transaction_ID
class Account(models.Model):
    user_id = models.CharField(max_length=200,unique=True,null=True)
    balance = models.IntegerField(default=10000)
    transaction = models.ManyToManyField(Transaction, related_name="transaction", null=True, blank=True)
    watchlist = models.TextField(default="", blank=True)
    # needs fixes

    def __str__(self):
        return self.user_id

