from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review, Product, ProductAttribute



@receiver(post_save, sender=Review)
def update_review_average(sender, instance, **kwargs):
    # Calculate the average rating for all reviews of the product
    product = instance.product
    reviews = Review.objects.filter(product=product)
    total_rating = 0
    for review in reviews:
        total_rating += int(review.rating)
    if reviews.count() > 0:
        product.review_average = total_rating / reviews.count()
    else:
        product.review_average = 0
    product.save()
    
    
@receiver(post_save, sender=ProductAttribute)
def update_product_woocommerce(sender, instance, created, **kwargs):
    if created:
        instance.product.status = 'VARIABLE'
        instance.product.attributes_type = instance.check_type_of_attribute()
        instance.product.save()
        

@receiver(post_save, sender=product_campaigns)
def create_campaign_owner(sender, instance, created, **kwargs):
    if created:
        if daily_items.objects.filter(product=instance.product).exists():
            pass
        else:
            new_daily_item = daily_items(product=instance.product)
            new_daily_item.save()
      
