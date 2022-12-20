from django import template
import calendar

register = template.Library()


@register.filter
def number_to_month(month_number):
    month_number = int(month_number)
    return calendar.month_abbr[month_number]