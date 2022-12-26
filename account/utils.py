from .models import *

def main_type_data_set(main_type_model, selected_month, user):
    """Return a set of data for income and expense models seperately"""

    #get the name of the model
    nature = main_type_model.__name__

    #get all the transactions for selected month
    selected_month_data = main_type_model.objects.filter(date__month=selected_month, user=user)

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

    #total amount for selected month
    selected_month_total = sum(selected_month_data.values_list('amount', flat=True))
        
    #monthly change
    previous_month = (selected_month - 1) if selected_month > 1  else 12
    previous_month_data = main_type_model.objects.filter(date__month=previous_month, user=user)
    previous_month_total = sum(previous_month_data.values_list('amount', flat=True))
    monthly_change = round(selected_month_total - previous_month_total, 2)


    data_set = {
        'nature': nature,
        'transaction_count': transaction_count,
        'selected_month_total': selected_month_total,
        'monthly_change': monthly_change,
    }
    return data_set


def manual_adjustment(model, date, bank, user):
    adjustment, _ = model.objects.get_or_create(
        detail = 'Manual adjustment',
        date = date,
        bank = bank,
        user = user,
        category = 'Manual adjustment'
    )
    return adjustment


def get_object_or_none(model, id, user):
    try:
        return model.objects.get(id=id, user=user)
    except model.DoesNotExist:
        return None

