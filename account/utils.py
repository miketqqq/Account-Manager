from .models import *
from chart.utils import current_month


def main_type_data_set(main_type_model, selected_month):
    """Return a set of data for income and expense models seperately"""

    #get the name of the model
    nature = main_type_model.__name__

    #get all the transactions for selected month
    selected_month_data = main_type_model.objects.filter(date__month=selected_month)

    #if no transaction for that month, return 0
    if not selected_month_data:
        data_set = {
            'nature': nature,
            'transaction_count': 0,
            'current_month_total': 0,
            'monthly_change': 0,
        }
        return data_set
        
    #transaction count
    transaction_count = selected_month_data.count()

    #get total amount for selected month
    selected_month_total = sum(selected_month_data.values_list('amount', flat=True))
        
    #monthly change
    previous_month = (selected_month - 1) if selected_month > 1  else 12
    previous_month_data = main_type_model.objects.filter(date__month=previous_month)
    previous_month_total = sum(previous_month_data.values_list('amount', flat=True))
    monthly_change = round(selected_month_total - previous_month_total, 2)


    data_set = {
        'nature': nature,
        'transaction_count': transaction_count,
        'selected_month_total': selected_month_total,
        'monthly_change': monthly_change,
    }
    return data_set


def displayed_month(request):
    """get the user's selection, or use current month as default"""

    return int(request.session['display_date']['month'])


def get_object_or_none(model, id, user):
    try:
        return model.objects.get(id=id, user=user)
    except model.DoesNotExist or model.MultipleObjectsReturned:
        return None





""" def monthly_change(grouped_data, current_data, select_date=today): 
    previous_month = (select_date.replace(day=1) - datetime.timedelta(days=1)).month

    try:
        previous_data = grouped_data.get(
            by_month__month=previous_month)['sub_total']
    except ObjectDoesNotExist:
        previous_data = 0

    change = round(current_data - previous_data, 0)
    return change"""

"""def get_month_total(grouped_data, selected_month):
    #get sub total for a specific month.
    
    try:
        current_month_total = grouped_data.get(
            by_month__month=selected_month)['sub_total']
    except ObjectDoesNotExist:
        current_month_total = 0
    return current_month_total"""