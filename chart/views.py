from django.http import JsonResponse
from django.db.models import Q

# Create your views here.
from account.models import * 
from chart import utils as chart_utils
from statistics import mean 
from dateutil.relativedelta import relativedelta
import datetime

def income_expense_chart(request):
    """data for line chart"""    
    
    display_month = request.session['display_month']
    display_year = request.session['display_year']
    display_month_year = datetime.datetime(
        year=display_year, 
        month=display_month, 
        day=1
    )

    #get the upper and lower bound of 12 months
    last_day = chart_utils.last_day_of_month(display_month_year)  
    month_label = display_month_year + relativedelta(months=-11)  #the earliest month
    
    income = Income.objects.filter(
        Q(date__lte=last_day),
        Q(date__gte=month_label),
        user=request.user
    ).exclude(category='Manual adjustment')
    
    expense = Expense.objects.filter(
        Q(date__lte=last_day),
        Q(date__gte=month_label),
        user=request.user
    ).exclude(category='Manual adjustment')

    income_by_month_data = chart_utils.group_by_month(income)
    expense_by_month_data = chart_utils.group_by_month(expense)

    labels = [None] * 12
    income_data = [None] * 12
    expense_data = [None] * 12
    
    for index in range(12):
        #get a list of income for the latest 12 months
        if data := income_by_month_data.filter(
            by_month__month=month_label.month,
            by_month__year=month_label.year
        ):
            income_data[index] = data[0]['sub_total']
        else:
            income_data[index] = 0

        #get a list of expense for the latest 12 months
        if data := expense_by_month_data.filter(
            by_month__month=month_label.month,
            by_month__year=month_label.year
        ):
            expense_data[index] = data[0]['sub_total']
        else:
            expense_data[index] = 0
        
        #format the month label (for x-axis)
        labels[index] = month_label.strftime("%b %y")

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
    banks = BankAccount.objects.filter(user=request.user).values('bank_name', 'balance')

    if not banks:
        label = ['Example']
        balance = [10]
    else:
        label = list(banks.values_list('bank_name', flat=True))
        balance = list(banks.values_list('balance', flat=True))

    context = {
        'label': label,
        'balance': balance,
    }
    return JsonResponse(context)

def category_chart(request):
    """group category by month for bar chart"""
    selected_month = request.session['display_month']
    selected_year = request.session['display_year']

    income_category_data = chart_utils.category_data_set(
        Income, selected_month, 
        selected_year, request.user
    )
    expense_category_data = chart_utils.category_data_set(
        Expense, selected_month, 
        selected_year, request.user
    )

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