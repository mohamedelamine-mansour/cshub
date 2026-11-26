from django import template

register = template.Library()


@register.filter
def bootstrap(field):
    widget = field.field.widget
    kind = getattr(widget, 'input_type', '')
    css = {
        'select': 'form-select',
        'checkbox': 'form-check-input',
    }.get(kind, 'form-control')
    if field.errors:
        css += ' is-invalid'
    return field.as_widget(attrs={'class': css})