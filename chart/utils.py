from django.db.models import Sum
from django.db.models.functions import TruncMonth, Round

from statistics import mean 
import datetime

today = datetime.date.today()
current_month = today.month

def group_by_month(transaction_data, sub_type='nature'):
    """group data by month or category."""

    grouped_data = transaction_data\
        .annotate(by_month=TruncMonth('date'))\
        .values('by_month', sub_type)\
        .annotate(sub_total=Round(Sum('amount'), precision=2))\
        .order_by('by_month')
    return grouped_data


def monthly_average(grouped_data):
    avg = grouped_data\
        .filter(by_month__lte=today)\
        .values_list('sub_total', flat=True)
    return round(mean(avg), 0)


def category_data_set(main_type_model, selected_month, user):
    """Return a set of data grouped by category for income/expense seperately"""

    #data filtered by selected month
    main_data = main_type_model.objects.filter(date__month=selected_month, user=user).values('amount', 'category')

    #group by category
    category_current_month = main_data\
        .values('category')\
        .annotate(sub_total=Round(Sum('amount'), precision=2))\
        .order_by('-sub_total')

    return category_current_month

