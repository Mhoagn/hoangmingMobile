from django.db import models
from products.models import ProductVariant
from accounts.models import User


# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)  # cho guest
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING    = 'pending',    'Chờ xác nhận'
        CONFIRMED  = 'confirmed',  'Đã xác nhận'
        SHIPPING   = 'shipping',   'Đang giao'
        DELIVERED  = 'delivered',  'Đã giao'
        CANCELLED  = 'cancelled',  'Đã hủy'

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    code = models.CharField(max_length=20, unique=True)   # ORD-20240425-001
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    shipping_address = models.JSONField()      # snapshot địa chỉ lúc đặt hàng
    total_price = models.DecimalField(max_digits=14, decimal_places=0)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT)
    product_name = models.CharField(max_length=200)   # snapshot tên lúc đặt
    variant_info = models.CharField(max_length=100)   # "256GB - Titan Đen"
    price = models.DecimalField(max_digits=12, decimal_places=0)
    quantity = models.PositiveIntegerField()