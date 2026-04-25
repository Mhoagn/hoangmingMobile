from django.db import models

# Create your models here.
from django.db import models
from orders.models import Order

class Payment(models.Model):
    class Method(models.TextChoices):
        COD   = 'cod',   'Thanh toán khi nhận hàng'
        VNPAY = 'vnpay', 'VNPay'

    class Status(models.TextChoices):
        PENDING  = 'pending',  'Chờ thanh toán'
        PAID     = 'paid',     'Đã thanh toán'
        FAILED   = 'failed',   'Thất bại'
        REFUNDED = 'refunded', 'Đã hoàn tiền'

    order          = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    method         = models.CharField(max_length=10, choices=Method.choices)
    status         = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    amount         = models.DecimalField(max_digits=14, decimal_places=0)
    transaction_id = models.CharField(max_length=200, blank=True)  # chỉ có giá trị khi dùng VNPay
    paid_at        = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Payment #{self.order.code} - {self.get_method_display()}"