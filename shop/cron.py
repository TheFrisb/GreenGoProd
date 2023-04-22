from .models import Cart
from datetime import datetime, timedelta
import datetime
from django.utils import timezone

def old_carts_cleaner():
    two_days_ago = timezone.now() - timezone.timedelta(days=2)
    Cart.objects.filter(created_at__lt=two_days_ago).delete()

    
def reverse_offer_if_older_than_1_day():
    # get all carts older than 1 day
    one_day_ago = timezone.now() - timezone.timedelta(days=1)
    carts = Cart.objects.filter(created_at__lt=one_day_ago)
    for cart in carts:
        cart.has_viewed_checkout_offer = False
        cart.has_viewed_checkout_offer_time = None
        cart.has_accepted_checkout_offer = False
        cart.save()
