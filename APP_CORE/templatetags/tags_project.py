from django import template

# put your project-wide template tags here
# tags declared here gets registered in TEMPLATE.OPTIONS.Libraries
# use {% load tags_project %} in templates to use
register = template.Library()

@register.simple_tag
def project_hello(key):
    return "hello project tag"
