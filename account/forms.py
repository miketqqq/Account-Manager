from django import forms
from django.forms import ModelForm
from .models import *


class BankAccountForm(ModelForm):
    class Meta:
         model = BankAccount
         exclude = ['date','user']

class IncomeForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(IncomeForm, self).__init__(*args, **kwargs)
        self.fields['bank'].queryset = BankAccount.objects.filter(user=user)

    class Meta:
         model = Income
         exclude = ['user', 'nature']
         widgets = {
            'date': forms.DateInput(format=('%Y-%m-%d'),
            attrs={'type':'date'})
        } 

class ExpenseForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.fields['bank'].queryset = BankAccount.objects.filter(user=user)

    class Meta:
         model = Expense
         exclude = ['user', 'nature']
         widgets = {
            'date': forms.DateInput(format=('%Y-%m-%d'),
            attrs={'type':'date'})
        } 

