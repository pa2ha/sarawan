from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum
from slugify import slugify

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=50,
                            unique=True,
                            verbose_name='Название категории')
    slug = models.SlugField(unique=True,
                            blank=True,
                            verbose_name='Slug категории')
    image = models.ImageField(blank=True,
                              null=True,
                              upload_to='category/',
                              verbose_name='Изображение для категории')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=50,
                            unique=True,
                            verbose_name='Название подкатегории')
    slug = models.SlugField(unique=True,
                            blank=True,
                            verbose_name='Slug подкатегории')
    image = models.ImageField(blank=True,
                              null=True,
                              upload_to='subcategory/',
                              verbose_name='Изображение для подкатегории')
    category_id = models.ForeignKey(Category,
                                    on_delete=models.CASCADE,
                                    verbose_name='Категория подкатегории')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50,
                            unique=True,
                            verbose_name='Название продукта')
    slug = models.SlugField(unique=True,
                            blank=True,
                            verbose_name='Slug продукта')
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                verbose_name='Цена продукта')
    image_original = models.ImageField(upload_to='products/original/',
                                       null=True,
                                       blank=True,
                                       verbose_name='Оригинальное изображение')
    image_medium = models.ImageField(upload_to='products/medium/',
                                     null=True,
                                     blank=True,
                                     verbose_name='Среднее изображение')
    image_small = models.ImageField(upload_to='products/small/',
                                    null=True,
                                    blank=True,
                                    verbose_name='Маленькое изображение')
    sub_category_id = models.ForeignKey(SubCategory,
                                        on_delete=models.CASCADE,
                                        verbose_name='Подкатегория товара')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                verbose_name='Пользователь')
    items = models.ManyToManyField(Product,
                                   through='CartItem',
                                   verbose_name='Продукты')

    def calculate_total_quantity(self):
        return self.items.aggregate(
            total_quantity=Sum('cartitem__quantity'))['total_quantity'] or 0

    def calculate_total_cost(self):
        return (self.items
                .aggregate(total_cost=Sum(models.F(
                    'cartitem__quantity') * models.F('price'),
                    output_field=models.DecimalField()))['total_cost'] or 0)

    def clear_cart(self):
        self.items.clear()

    class Meta:
        ordering = ('user',)
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart,
                             on_delete=models.CASCADE,
                             verbose_name='корзина')
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                verbose_name='продукт')
    quantity = models.PositiveIntegerField(default=1,
                                           verbose_name='колличество')
