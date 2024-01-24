from django.contrib import admin
from products.models import Cart, CartItem, Category, Product, SubCategory


class CategoryAdmin(admin.ModelAdmin):

    list_display = [field.name for field in Category._meta.fields]


admin.site.register(Category, CategoryAdmin)


class SubCategoryAdmin(admin.ModelAdmin):

    list_display = [field.name for field in SubCategory._meta.fields]


admin.site.register(SubCategory, SubCategoryAdmin)


class ProductAdmin(admin.ModelAdmin):

    list_display = [field.name for field in Product._meta.fields]


admin.site.register(Product, ProductAdmin)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1  # Количество дополнительных форм для ввода


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'calculate_total_quantity', 'calculate_total_cost')
    inlines = [CartItemInline]


admin.site.register(Cart, CartAdmin)
