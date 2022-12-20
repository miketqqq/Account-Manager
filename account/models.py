from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal

# Create your models here.
"""
class user(models.Model):
    pass
"""

class BankAccount(models.Model):
    account_type = (
        ('Cash', 'Cash'), 
        ('Saving', 'Saving'),
        ('Credit card', 'credit Card')) 

    bank_name = models.CharField(max_length=50)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    account_type = models.CharField(max_length=100, choices = account_type, default='Cash')
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def alter_balance(self, operation, nature, amount):
        if nature == 'income' and operation == 'add' or \
            nature == 'expense' and operation == 'deduct':
            self.total_amount += amount
        else:
            self.total_amount -= amount
        self.save()

    def __repr__(self):
        return f"Bank_account(\
            bank_name={self.bank_name},\
            total_amount={self.total_amount},\
            date={self.date},\
            user={self.user})"

    def __str__(self):
        return self.bank_name

    class Meta:
        ordering = ['-date']

"""class Credit_card(models.Model):
    bank = models.ForeignKey(Bank_account, on_delete=models.CASCADE, null=True, Blank=Ture)
    credit_amount = models.DecimalField(max_digits=12, decimal_places=2)
    debt = models.DecimalField(max_digits=12, decimal_places=2)
    due_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
"""

class Transaction(models.Model):
    detail = models.CharField(max_length=100)
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))])
    date = models.DateField()
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
        ('Internal Transfer', 'Internal Transfer'),
        ('Other', 'Other'),
    ]
    nature = models.CharField(default='expense', editable=False, max_length=10)
    category = models.CharField(max_length=40, choices=expense_category)


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
        ('Internal Transfer', 'Internal Transfer'),
        ('Other', 'Other'),
    ]
    nature = models.CharField(default='income', editable=False, max_length=10)
    category = models.CharField(max_length=40, choices=income_category)

    def __repr__(self):
        return f"Income(detail={self.detail}, {self.amount}, {self.category}, {self.date})"

    def __str__(self):
        return f'{self.detail}, {self.amount}, {self.category}, {self.date}'
        
    class Meta:
        ordering = ['-date']

class CustomExpense(Transaction):
    custom_expense_category = [('a','a')]
    custom_category = models.CharField(max_length=40)
    is_income = models.CharField(default='expense', editable=False, max_length=10)


    def __str__(self):
        return self.custom_category

class CustomIncome(Transaction):
    custom_category = models.CharField(max_length=40)
    is_income = models.CharField(default='income', editable=False, max_length=10)


    def __str__(self):
        return self.custom_category


"""class MyModelFilter(django_filters.FilterSet):
    Expense = django_filters.ModelMultipleChoiceFilter(
        queryset=Expense.objects.all() + Custom_Expense.objects.filter(user=request.user)
def departments(request):
    if request is None:
        return Department.objects.none()

    company = request.user.company
    return company.department_set.all()

class EmployeeFilter(filters.FilterSet):
    department = filters.ModelChoiceFilter(queryset=departments)

"""