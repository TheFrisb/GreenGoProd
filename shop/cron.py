from .models import Cart
from datetime import datetime, timedelta
import datetime
from django.utils import timezone

def old_carts_cleaner():
    two_days_ago = timezone.now() - timezone.timedelta(days=2)
    Cart.objects.filter(created_at__lt=two_days_ago).delete()
