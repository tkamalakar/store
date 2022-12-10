from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from .models import *

class  CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        exclude = ('created_at', 'updated_at')

class UnitMeasureSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = MeasureUnit
        exclude = ('created_at', 'updated_at')

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        exclude = ('created_at', 'updated_at')

class CategorySerialzer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)

class BrandSerializer(WritableNestedModelSerializer,serializers.ModelSerializer):
    manufacturer = ManufacturerSerializer()
    class Meta:
        model = Brand
        exclude = ('created_at', 'updated_at')

class ProductSerializer(WritableNestedModelSerializer,serializers.ModelSerializer):
    brand = BrandSerializer()
    unit_of_measure = UnitMeasureSerilaizer()
    origin_country = CountrySerializer()
    class Meta:
        model = Product
        exclude = ('created_at', 'updated_at')


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name',)


class CategoryDetailSerialzer(WritableNestedModelSerializer, serializers.ModelSerializer):
    sub_categories = serializers.SerializerMethodField(required=False)
    products = ProductCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'products','sub_categories',)

    def get_sub_categories(self, obj):
        print(obj.id)
        try:
            category_list = CategorySerialzer(Category.objects.filter(parent_category=obj.id),many=True).data
            return category_list
        except Exception:
            return []
