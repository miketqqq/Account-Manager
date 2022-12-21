from django import template
import calendar

register = template.Library()


@register.filter
def number_to_month(month_number):
    if not month_number:
        return 'NA'
    if month_number > 12 or month_number < 1 :
        return 'to_be_amened'
    month_number = int(month_number)
    return calendar.month_abbr[month_number]