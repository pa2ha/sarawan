from rest_framework import serializers

from .models import Cart, Category, Product, SubCategory


class CategoryForSubCategory(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('__all__')


class SubCategoryForProduct(serializers.ModelSerializer):
    category_id = CategoryForSubCategory(read_only=True)

    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'slug', 'image', 'category_id')


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('__all__')


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True,
                                          read_only=True,
                                          source='subcategory_set')

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'image', 'subcategories')


class ProductSerializer(serializers.ModelSerializer):
    sub_category_id = SubCategoryForProduct(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug',
                  'image_original', 'image_medium', 'image_small',
                  'sub_category_id')


class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_quantity = serializers.SerializerMethodField()
    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['items', 'total_quantity', 'total_cost']

    def get_total_quantity(self, obj):
        return obj.calculate_total_quantity()

    def get_total_cost(self, obj):
        return obj.calculate_total_cost()
