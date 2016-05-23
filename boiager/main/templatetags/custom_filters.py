from django import template
import calendar
import locale

locale.setlocale(locale.LC_ALL, 'ca_ES.UTF-8')

register = template.Library()

@register.filter(name='month_name')
def month_name(num):
    return calendar.month_name[int(num)]
