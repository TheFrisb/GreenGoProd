from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review, Product



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
