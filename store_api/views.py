from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Category,Product
from .serializers import CategorySerialzer,CategoryDetailSerialzer,ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerialzer

    def list(self, request, *args, **kwargs):
        category_list = Category.objects.filter(category_type='root')
        serializer = CategorySerialzer(category_list, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        category = Category.objects.get(id=pk)
        serializer = CategoryDetailSerialzer(category)
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        product_list = Product.objects.all()
        serializer = ProductSerializer(product_list, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)