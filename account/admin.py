from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(BankAccount)
admin.site.register(Expense)
admin.site.register(Income)
admin.site.register(CustomExpense)
admin.site.register(CustomIncome)