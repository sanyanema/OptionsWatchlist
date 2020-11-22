# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Stock(models.Model):
    users = models.ManyToManyField(User, related_name="users")
    name = models.CharField(max_length=200,unique=True)
    transactions = models.ManyToManyField(User, related_name="transactions")

    def __str__(self):
        return self.name

class Transaction(models.Model):
    transaction_ID = models.IntegerField()
    date = models.DateField()
    closed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
class Account(models.Model):
    user_id = models.CharField(max_length=200,unique=True,null=True)
    balance = models.IntegerField(default=10000)
    transaction = models.ManyToManyField(Transaction, related_name="transaction", null=True)

    def __str__(self):
        return self.user_id

