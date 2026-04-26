from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product-list'),
    path('add-product/', views.add_product, name='add-product'),
    path('<int:product_id>/update/', views.update_product, name='update-product'),
    path('brands/add-brand/', views.add_brand, name='add-branch'),
    path('brands/', views.get_brands, name='get-brands'),
    path('categories/', views.get_categories, name='get-categories'),
    path('categories/add-category/', views.add_category, name='add-category'),
    path('<int:product_id>/variants/', views.get_product_variants),       
    path('<int:product_id>/variants/add/', views.add_product_variant), 
    path('variants/<int:variant_id>/images/add/', views.add_product_image),   
]