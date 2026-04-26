from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, Product,Brand, ProductImage, ProductVariant
from .serializers import CategorySerializer, ProductImageSerializer, ProductSerializer, BrandSerializer, ProductVariantSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import permission_classes
import cloudinary.uploader

# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_brand(request):
    if not request.user.is_admin:
        return Response({'message': 'Bạn không có quyền thực hiện hành động này'}, status=403)
    name = request.data.get('name')
    if not name:
        return Response({'message': 'Tên thương hiệu không được để trống'}, status=400)
    
    brand = Brand.objects.filter(name=name).first()
    if brand:
        return Response({'message': 'Thương hiệu đã tồn tại'}, status=400)
    
    serializer = BrandSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_brands(request):
    brands = Brand.objects.all()
    serializer = BrandSerializer(brands, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_category(request):
    if not request.user.is_admin:
        return Response({'message': 'Bạn không có quyền thực hiện chức năng này'}, status=403)

    name = request.data.get('name')
    parent_id = request.data.get('parent_id')

    if not name:
        return Response({'message': 'Tên danh mục không được để trống'}, status=400)

    parent = None
    if parent_id:
        try:
            parent = Category.objects.get(id=parent_id)
        except Category.DoesNotExist:
            return Response({'message': 'Danh mục cha không tồn tại'}, status=400)

    if Category.objects.filter(name=name, parent=parent).exists():
        return Response({'message': 'Danh mục đã tồn tại'}, status=400)

    # Tạo trực tiếp thay vì qua serializer vì đã validate thủ công rồi
    category = Category.objects.create(name=name, parent=parent)
    return Response(CategorySerializer(category).data, status=201)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_product(request):
    if not request.user.is_admin:
        return Response({'message': 'Bạn không có quyền thực hiện hành động này'}, status=403)
    name = request.data.get('name')
    brand_id = request.data.get('brand_id')
    category_id = request.data.get('category_id')
    description = request.data.get('description')
    if not all([name, brand_id, category_id, description]):
        return Response({'message': 'Tên, thương hiệu, danh mục và mô tả là bắt buộc'}, status=400)

    try:
        brand = Brand.objects.get(id=brand_id)
    except Brand.DoesNotExist:
        return Response({'message': 'Thương hiệu không tồn tại'}, status=400)
    
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response({'message': 'Danh mục không tồn tại'}, status=400)
    
    product = Product.objects.create(
        name=name, 
        brand=brand, 
        category=category,
        description=description
    )
    return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_product(request, product_id):
    if not request.user.is_admin:
        return Response({'message': 'Bạn không có quyền thực hiện hành động này'}, status=403)
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'message': 'Sản phẩm không tồn tại'}, status=404)

    name = request.data.get('name')
    brand_id = request.data.get('brand_id')
    category_id = request.data.get('category_id')
    description = request.data.get('description')

    if name:
        product.name = name
    if brand_id:
        try:
            brand = Brand.objects.get(id=brand_id)
            product.brand = brand
        except Brand.DoesNotExist:
            return Response({'message': 'Thương hiệu không tồn tại'}, status=400)
    if category_id:
        try:
            category = Category.objects.get(id=category_id)
            product.category = category
        except Category.DoesNotExist:
            return Response({'message': 'Danh mục không tồn tại'}, status=400)
    if description:  
        product.description = description

    product.save()
    return Response(ProductSerializer(product).data)

@api_view(['GET'])
def product_list(request):
    try:
        page = int(request.query_params.get('page', 1))
        limit = int(request.query_params.get('limit', 10))
    except ValueError:
        return Response({'message': 'Page và limit phải là số nguyên'}, status=400)
    
    offeset = (page - 1) * limit
    products = Product.objects.filter(is_active=True)[offeset: offeset + limit]
    total = Product.objects.filter(is_active=True).count()

    return Response({
        'total': total,
        'page': page,
        'limit': limit,
        'total_pages': (total + limit - 1) // limit,
        'results': ProductSerializer(products, many=True).data
    })

@api_view(['GET'])
def get_product_variants(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'message': 'Sản phẩm không tồn tại'}, status=404)

    variants = ProductVariant.objects.filter(product=product)
    return Response(ProductVariantSerializer(variants, many=True).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_product_variant(request, product_id):
    if not request.user.is_admin:
        return Response({'message': 'Bạn không có quyền thực hiện hành động này'}, status=403)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'message': 'Sản phẩm không tồn tại'}, status=404)

    color = request.data.get('color')
    storage = request.data.get('storage')
    price = request.data.get('price')
    sale_price = request.data.get('sale_price')
    stock = request.data.get('stock', 0)
    sku = request.data.get('sku')

    if not all([color, storage, price, sku]):
        return Response({'message': 'Màu sắc, dung lượng, giá và SKU là bắt buộc'}, status=400)

    if ProductVariant.objects.filter(sku=sku).exists():
        return Response({'message': 'SKU đã tồn tại'}, status=400)

    if ProductVariant.objects.filter(product=product, color=color, storage=storage).exists():
        return Response({'message': 'Phiên bản này đã tồn tại'}, status=400)

    variant = ProductVariant.objects.create(
        product=product,
        color=color,
        storage=storage,
        price=price,
        sale_price=sale_price,
        stock=stock,
        sku=sku
    )
    return Response(ProductVariantSerializer(variant).data, status=201)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_product_image(request, variant_id):
    if not request.user.is_admin:
        return Response({'message': 'Bạn không có quyền thực hiện hành động này'}, status=403)

    try:
        variant = ProductVariant.objects.get(id=variant_id)
    except ProductVariant.DoesNotExist:
        return Response({'message': 'Phiên bản sản phẩm không tồn tại'}, status=404)

    image_file = request.FILES.get('image')
    image_url = request.data.get('image_url')
    is_primary = request.data.get('is_primary', False)

    if not image_file and not image_url:
        return Response({'message': 'Ảnh là bắt buộc'}, status=400)

    if is_primary:
        ProductImage.objects.filter(variant=variant, is_primary=True).update(is_primary=False)

    # Upload file hoặc URL lên Cloudinary
    if image_file:
        uploaded = cloudinary.uploader.upload(image_file, folder='products/')
    else:
        uploaded = cloudinary.uploader.upload(image_url, folder='products/')

    product_image = ProductImage.objects.create(
        variant=variant,
        image=uploaded['secure_url'],  # lưu URL cloudinary trả về
        is_primary=is_primary,
        order=ProductImage.objects.filter(variant=variant).count() + 1
    )
    return Response(ProductImageSerializer(product_image).data, status=201)