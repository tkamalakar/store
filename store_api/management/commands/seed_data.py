import json
from django.core.management.base import BaseCommand

from store_api.models import * 


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        # Opening JSON file
        f = open('nat_first_data.json') 
        data = json.load(f)
        if data.get('users'):
            users = data.get('users')
            for user in users:
                User.objects.get_or_create(**user)
        if data.get('countries'):
            countries = data.get('countries')
            for country in countries:
                Country.objects.get_or_create(**country)
        if data.get('manufacturers'):
            manufacturers = data.get('manufacturers')
            for manufacturer in manufacturers:
                user = User.objects.get(id=manufacturer.get('created_by'))
                manufacturer['created_by'] = user
                country = Country.objects.get(code=manufacturer.get("country_code"))
                manufacturer["country_code"] = country
                manufacturer['created_by'] = user
                Manufacturer.objects.get_or_create(**manufacturer)
        if data.get('brands'):
            brands = data.get('brands')
            for brand in brands:
                man = brand.get('manufacturer')
                manufacturer = Manufacturer.objects.get(id=man)
                brand['manufacturer'] = manufacturer
                Brand.objects.get_or_create(**brand)
        if data.get('nutrients'):
            nutrients = data.get('nutrients')
            for nutrient in nutrients:
                Nutrient.objects.get_or_create(**nutrient)
        if data.get('ingredients'):
            ingredients = data.get('ingredients')
            for ingredient in ingredients:
                Ingredient.objects.get_or_create(**ingredient)
        if data.get('measure_units'):
            measure_units = data.get('measure_units')
            for measure_unit in measure_units:
                MeasureUnit.objects.get_or_create(**measure_unit)
        if data.get('products'):
            products = data.get('products')
            for product in products:
                unit_of_measure = MeasureUnit.objects.get(id=product.get("unit_of_measure"))
                product["unit_of_measure"] = unit_of_measure
                origin_country = Country.objects.get(code=product.get("origin_country"))
                product["origin_country"] = origin_country
                brand = Brand.objects.get(id=product.get("brand"))
                product["brand"] = brand
                created_by = User.objects.get(id=product.get("created_by"))
                product["created_by"] = created_by
                Product.objects.get_or_create(**product)
        if data.get('product_nutrients'):
            product_nutrients = data.get('product_nutrients')
            for product_nutrient in product_nutrients:
                product = Product.objects.get(id=product_nutrient.get('product'))
                nutrient = Nutrient.objects.get(id=product_nutrient.get('nutrient'))
                unit_of_measure = MeasureUnit.objects.get(id=product_nutrient.get('unit_of_measure'))
                product_nutrient['unit_of_measure'] = unit_of_measure
                product_nutrient['product'] = product
                product_nutrient['nutrient'] = nutrient
                ProductNutrient.objects.get_or_create(**product_nutrient)
        if data.get('product_ingredients'):
            product_ingredients = data.get('product_ingredients')
            for product_ingredient in product_ingredients:
                product = Product.objects.get(id=product_ingredient.get('product'))
                ingredient = Ingredient.objects.get(id=product_ingredient.get('ingredient'))
                unit_of_measure = MeasureUnit.objects.get(id=product_ingredient.get('unit_of_measure'))
                product_ingredient['unit_of_measure'] = unit_of_measure
                product_ingredient['product'] = product
                product_ingredient['ingredient'] = ingredient
                ProductIngredient.objects.get_or_create(**product_ingredient)
        if data.get('categories'):
            categories = data.get('categories')
            for category in categories:
                products = category.pop('products')
                cat,created = Category.objects.get_or_create(**category)
                for prod in products:
                    product = Product.objects.get(id=prod)
                    cat.products.add(product)
        f.close()
        print("objects unpacked")
