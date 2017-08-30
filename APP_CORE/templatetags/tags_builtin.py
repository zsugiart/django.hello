from django import template
from APP_CORE import config
# put your project-wide template tags here
register = template.Library()

@register.simple_tag
def ui_config(key):
    return config.key(key)

@register.simple_tag
def ui_label(key):
    return config.label(key)
