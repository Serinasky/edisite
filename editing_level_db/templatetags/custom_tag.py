from django import template

register = template.Library()

@register.filter(name="mysplit")
def mysplit(value, sep = ","):
	return value.split(",")