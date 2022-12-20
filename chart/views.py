from django.http import JsonResponse

# Create your views here.
from account.models import * 
from account.utils import displayed_month
from .utils import category_data_set, group_by_month
from statistics import mean 
from dateutil.relativedelta import relativedelta
import datetime

def income_expense_chart(request):
    """data for line chart"""
    income = Income.objects.all()
    expense = Expense.objects.all()
    #income = Income.objects.filter(user=request.user)
    #expense = Expense.objects.filter(user=request.user)

    income_by_month_data = group_by_month(income)
    expense_by_month_data = group_by_month(expense)

    labels = []
    income_data = []
    expense_data = []
    month_label = datetime.date.today() + relativedelta(months=-11) #the earliest month
    
    for _ in range(12):
        #get a list of income for the latest 12 months
        if data := income_by_month_data.filter(by_month__month=month_label.month):
            income_data.append(data[0]['sub_total'])
        else:
            income_data.append(0)

        #get a list of expense for the latest 12 months
        if data := expense_by_month_data.filter(by_month__month=month_label.month):
            expense_data.append(data[0]['sub_total'])
        else:
            expense_data.append(0)
        
        #format the month label (for x-axis)
        labels.append(month_label.strftime("%b %y"))

        #update the month
        month_label += relativedelta(months=+1)
        
    income_mean = round(mean(income_data), 0)
    expense_mean = round(mean(expense_data), 0)

    context = {
        'labels': labels,
        'income_data': income_data,
        'expense_data': expense_data,
        'income_mean': income_mean,
        'expense_mean': expense_mean,
    }
    return JsonResponse(context)

def bank_account_chart(request):
    """data for pie chart"""
    banks = BankAccount.objects.filter(user=request.user).values('bank_name', 'total_amount')

    label = list(banks.values_list('bank_name', flat=True))
    balance = list(banks.values_list('total_amount', flat=True))

    context = {
        'label': label,
        'balance': balance,
    }
    return JsonResponse(context)

def category_chart(request):
    """group category by month for bar chart"""
    selected_month = displayed_month(request)

    income_category_data = category_data_set(Income, selected_month, user=request.user)
    expense_category_data = category_data_set(Expense, selected_month, user=request.user)

    #income
    income_label = [data['category'] for data in income_category_data]
    income_amount = [data['sub_total'] for data in income_category_data]

    #expense
    expense_label = [data['category'] for data in expense_category_data]
    expense_amount = [data['sub_total'] for data in expense_category_data]

    context = {
        'income_label': income_label,
        'income_amount': income_amount,
        'expense_label': expense_label,
        'expense_amount': expense_amount,
    }

    return JsonResponse(context)