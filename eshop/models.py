from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length = 250, db_index = True)
    slug = models.SlugField(max_length = 250, db_index = True, unique = True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name
    

class Sort(models.Model):
    name = models.CharField(max_length = 200, db_index = True)

    class Meta:
        verbose_name = 'Сорт'
        verbose_name_plural = 'Сорта'

    def __str__(self):
        return self.name
    

class Country(models.Model):
    name = models.CharField(max_length = 200, db_index = True)

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self):
        return self.name


class Product(models.Model):
    categoryID = models.ForeignKey(Category, related_name = 'products', on_delete = models.CASCADE)
    sortID = models.ForeignKey(Sort, blank = True, null = True, on_delete = models.SET_NULL)
    countryID = models.ForeignKey(Country, blank = True, null = True, on_delete = models.SET_NULL)

    name = models.CharField(max_length = 250, db_index = True)
    slug = models.SlugField(max_length = 250, db_index = True)
    image = models.ImageField(upload_to = 'products', blank = True, null = True)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    description = models.TextField(blank = True)
    weight = models.DecimalField(max_digits = 5, decimal_places = 0, default = 0)
    available = models.BooleanField(default = True)

    class Meta:
        ordering = ('name', )
        indexes = [models.Index(fields = ['id', 'slug'])]
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product', kwargs = { 'id': self.id, 'slug': self.slug })


class Cart(models.Model):
    date = models.DateTimeField(auto_now_add = True)

    def get_total_amount(self):
        return sum(item.get_amount() for item in self.cart_items.all())


class CartItem(models.Model):
    cartID = models.ForeignKey(Cart, related_name = 'cart_items', on_delete = models.CASCADE)
    productID = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveBigIntegerField(default = 1)

    def get_amount(self):
        return self.productID.price * self.quantity


class Order(models.Model):
    clientID = models.ForeignKey(User, related_name = 'orders', on_delete = models.CASCADE)
    last_name = models.CharField(max_length = 250, default = 'Не указан')
    first_name = models.CharField(max_length = 250, default = 'Не указан')
    phone = models.CharField(max_length = 25, default = 'Не указан')
    address = models.CharField(max_length = 250, default = 'Не указан')
    date = models.DateTimeField(auto_now_add = True)
    paid = models.BooleanField(default = True)
    done = models.BooleanField(default = False)

    class Meta:
        ordering = ('date', )
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def get_total_amount(self):
        return sum(item.get_amount() for item in self.order_items.all())
    
    def get_total_weight(self):
        return sum(item.get_weight() for item in self.order_items.all())


class OrderItem(models.Model):
    orderID = models.ForeignKey(Order, related_name = 'order_items', on_delete = models.CASCADE)
    productID = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveBigIntegerField(default = 1)

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    def get_amount(self):
        return self.productID.price * self.quantity
    
    def get_weight(self):
        return self.productID.weight