from django.db import models

from products.models import Product
from accounts.models import User
from orders.models import OrderItem

# Create your models here.
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_item = models.OneToOneField(OrderItem, on_delete=models.SET_NULL, null=True)
    rating = models.PositiveSmallIntegerField()      # 1-5
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')        # 1 user chỉ review 1 lần/sản phẩm