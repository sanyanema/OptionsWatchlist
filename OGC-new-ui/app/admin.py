# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import Transaction, Account

# Register your models here.
admin.site.register(Transaction)
admin.site.register(Account)
