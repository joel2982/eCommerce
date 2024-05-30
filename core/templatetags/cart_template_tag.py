from django import template
from core.models import Order

register = template.Library()

@register.filter
def cart_count(user):
    if user.is_authenticated:
        cart = Order.objects.filter(user=user, ordered=False).first()
        if cart:
            count = 0
            for item in cart.order_items.all():
                count += item.quantity
            return count
    return 0