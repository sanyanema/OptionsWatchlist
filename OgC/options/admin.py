from django.contrib import admin
from .models import Option 
# Register your models here.
class OptionAdmin(admin.ModelAdmin):
    list_display = ("name",)
admin.site.register(Option, OptionAdmin)