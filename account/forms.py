from django import forms
from django.forms import ModelForm
from .models import *


class BankAccountForm(ModelForm):
    class Meta:
         model = BankAccount
         exclude = ['date','user']

class IncomeForm(ModelForm):
    class Meta:
         model = Income
         exclude = ['user', 'nature']
         widgets = {
            'date': forms.DateInput(format=('%Y-%m-%d'),
            attrs={'type':'date'})
        } 

class ExpenseForm(ModelForm):
    class Meta:
         model = Expense
         exclude = ['user', 'nature']
         widgets = {
            'date': forms.DateInput(format=('%Y-%m-%d'),
            attrs={'type':'date'})
        } 


"""
#category = forms.ChoiceField(choices=gather_choices)
def gather_choices():
    customs = CustomExpense.objects.all()
    custom_choices=[]
    for custom in customs:
        new_item = (f"{custom.custom_category}", f"{custom.custom_category}")
        custom_choices.append(new_item)
    return Expense.expense_category + custom_choices"""
