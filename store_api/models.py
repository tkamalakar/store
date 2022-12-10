from django.db import models
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import AbstractUser

CATEGORY_TYPE = (("root", "root"), ("sub", "sub"))


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @classmethod
    def to_date_time(self, timestamp):
        return datetime.fromtimestamp(timestamp)

    @classmethod
    def to_timestamp(self, time):
        return datetime.timestamp(time)


class Country(BaseModel):
    code = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=30)
    continent = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class User(AbstractUser):
    full_name = models.CharField(max_length=50)
    country_code = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.full_name


class Manufacturer(BaseModel):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    country_code = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Brand(BaseModel):
    name = models.CharField(max_length=50)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class MeasureUnit(BaseModel):
    unit_of_measure = models.CharField(max_length=15)
    type = models.CharField(max_length=15)


class Product(BaseModel):
    barcode = models.BigIntegerField()
    name = models.CharField(max_length=150)
    fssai_lic_no = models.BigIntegerField()
    unit_of_measure = models.ForeignKey(MeasureUnit, on_delete=models.PROTECT)
    measure_fact = models.IntegerField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    best_before = models.CharField(max_length=30)
    mrp = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    origin_country = models.ForeignKey(
        Country, on_delete=models.PROTECT,  null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Nutrient(BaseModel):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class ProductNutrient(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    unit_of_measure = models.ForeignKey(MeasureUnit, on_delete=models.PROTECT)
    measure_fact = models.IntegerField()


class Ingredient(BaseModel):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class ProductIngredient(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    unit_of_measure = models.ForeignKey(MeasureUnit, on_delete=models.PROTECT)
    measure_fact = models.IntegerField()


class Category(BaseModel):
    name = models.CharField(max_length=150)
    category_type = models.CharField(choices=CATEGORY_TYPE, max_length=20)
    parent_category = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    products = models.ManyToManyField(Product, related_name="categories")

    def __str__(self):
        return self.name
