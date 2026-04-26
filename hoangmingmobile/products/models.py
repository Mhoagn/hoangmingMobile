from django.db import models

# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)


    def __str__(self):
        return self.name    
    
class Product(models.Model):
    name = models.CharField(max_length=200)          
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ProductVariant(models.Model):
    """Mỗi variant là 1 phiên bản cụ thể: màu sắc + dung lượng"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    color = models.CharField(max_length=50)          # Titan Đen, Xanh Sa Mạc
    storage = models.CharField(max_length=20)        # 128GB, 256GB, 512GB
    price = models.DecimalField(max_digits=12, decimal_places=0)
    sale_price = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=100, unique=True)

class ProductImage(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='images')
    image = models.CharField(max_length=500)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)

class ProductSpec(models.Model):
    """Thông số kỹ thuật dạng key-value, linh hoạt cho mọi dòng máy"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specs')
    name = models.CharField(max_length=100)          # "Màn hình", "Camera", "Pin"
    value = models.CharField(max_length=255)         # "6.7 inch OLED", "48MP"
    order = models.PositiveSmallIntegerField(default=0)