from django import template

register = template.Library()

# todo/templatetags/custom_filters.py

from django import template
from django.apps import apps

register = template.Library()

@register.filter
def get_verbose_name(field_name, model_path):
    app_label, model_name = model_path.split(".")
    model = apps.get_model(app_label, model_name)
    try:
        return model._meta.get_field(field_name).verbose_name
    except Exception:
        return field_name

@register.filter
def not_in(value, arg_list):
    return value not in arg_list.split(',')


