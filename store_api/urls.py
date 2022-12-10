from django.urls import re_path
from rest_framework import routers
from . import views
from django.urls import path

router = routers.SimpleRouter()
router.register(r'categories', views.CategoryViewSet, basename='categories')
router.register(r'products', views.ProductViewSet, basename='products')
urlpatterns = [
]
urlpatterns += router.urls