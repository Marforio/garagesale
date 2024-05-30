from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('dashboard/add_product/', views.add_product, name='add_product'),
    path('dashboard/product_added/', views.product_add_success, name='product_add_success'),
    path('dashboard/', views.order_list, name='order_list'),
    path('dashboard/<str:settled_or_open>/', views.order_list, name='order_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:product_id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('order/<int:product_id>/<slug:slug>/', views.product_order, name='product_order'),
    path('order/success/', views.order_success, name='order_success'),
]
