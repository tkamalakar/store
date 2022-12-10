from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(MeasureUnit)
admin.site.register(Ingredient)
admin.site.register(Country)
admin.site.register(Manufacturer)
admin.site.register(Brand)
admin.site.register(Nutrient)
admin.site.register(ProductNutrient)
admin.site.register(ProductIngredient)
