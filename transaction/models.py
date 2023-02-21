""" from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal

# Create your models here.
from account.models import BankAccount
import uuid


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    detail = models.CharField(max_length=100)
    amount = models.DecimalField(
        default=0,
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))])
    date = models.DateField(default=timezone.now)
    bank = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
        
    def __str__(self):
        return f'{self.detail}, {self.amount}, {self.date}, {self.bank}'
    
    class Meta:
        ordering = ['-date']
    #    abstract = True


class Expense(Transaction):
    expense_category = [
        ('Food', 'Food'),
        ('Transport', 'Transport'),
        ('Rent', 'Rent'),
        ('Bill', 'Bill'),
        ('Entertainment', 'Entertainment'),
        ('Shopping', 'Shopping'),
        ('Manual adjustment', 'Manual adjustment'),
        ('Other', 'Other'),
    ]
    nature = models.CharField(default='expense', editable=False, max_length=10)
    category = models.CharField(max_length=40, choices=expense_category)
    #category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)

    def __repr__(self):
        return f"Expense(detail={self.detail}, {self.amount}, {self.category}, {self.date})"

    def __str__(self):
        return f'{self.detail}, {self.amount}, {self.category}, {self.date}'
    
    class Meta:
        ordering = ['-date']


class Income(Transaction):
    income_category = [
        ('Salary', 'Salary'),
        ('Investment', 'Investment'),
        ('Online Shop', 'Online Shop'),
        ('Manual adjustment', 'Manual adjustment'),
        ('Other', 'Other'),
    ]
    nature = models.CharField(default='income', editable=False, max_length=10)
    category = models.CharField(max_length=40, choices=income_category)
    #category = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE)

    def __repr__(self):
        return f"Income(detail={self.detail}, {self.amount}, {self.category}, {self.date})"

    def __str__(self):
        return f'{self.detail}, {self.amount}, {self.category}, {self.date}'
        
    class Meta:
        ordering = ['-date']


class IncomeCategory(models.Model):
    category = models.CharField(max_length=40)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __repr__(self):
        return f"category={self.category}, user={self.user}"

    def __str__(self):
        return self.category


class ExpenseCategory(models.Model):
    category = models.CharField(max_length=40)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __repr__(self):
        return f"category={self.category}, user={self.user}"

    def __str__(self):
        return self.category
 """
