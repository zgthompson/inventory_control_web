from django import template
from inventory_control import config

register = template.Library()

@register.assignment_tag
def get_site_name():
    return config.SITE_NAME
