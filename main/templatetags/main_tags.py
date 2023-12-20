from django import template

register = template.Library()

@register.filter(name='date_contains')
def date_contains(queryset, day):
    return any(item.date.day == int(day) for item in queryset)
