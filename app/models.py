import random
from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):

    phone = models.CharField(max_length=13)
    email = models.EmailField()
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created = models.DateTimeField(blank=True, null=True)

    def generat_otp(self):
        from django.utils.timezone import now
        self.otp = str(random.randint(10000, 99999))
        self.otp_created = now()
        self.save()

    def otp_is_valid(self):
        from datetime import timedelta
        from django.utils.timezone import now
        return now() - self.otp_created < timedelta(minutes=5)
    
    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.ImageField(upload_to='images/category/', blank=True, default='/images/default.jpg')

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True, default='No description available')
    price = models.FloatField()
    discount = models.IntegerField(blank=True, default=0)
    image_url = models.ImageField(upload_to='images/products/', blank=True, default='/images/default.jpg')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    favorited_by = models.ManyToManyField(MyUser, related_name='favorite_products', blank=True)
    dicountedPrice = models.IntegerField(blank=True, default=0)

    def save(self, force_insert = ..., force_update = ..., using = ..., update_fields = ...):
        self.dicountedPrice = self.price - (self.price * (self.discount/100))
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.name

class Delevry(models.Model):
    # !!!!!!!i will modify this model like a user model

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Address(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    lang = models.FloatField()
    lat = models.FloatField()
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} of {self.user.username}'
    
class Order(models.Model):
    STATUS_CHOICES= [(1, 'Pending'), (2, 'Accepted'), (3, 'Processing'), (4, 'Delivered'), (5, 'Canceled')]
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    delivery = models.ForeignKey(Delevry, on_delete=models.CASCADE, blank=True, null=True)
    total_price = models.FloatField()
    quantity = models.IntegerField()
    payment_method = models.CharField(max_length=100, choices=[('Cash', 'cash'), ('Credit', 'credit')])
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} at {self.date.date()}'
    
class Cart(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'product', 'order'], name='unique_user_product_cart')]

    def __str__(self):
        if self.order:
            return f'{self.product.name}, of: {self.user.username}, inOrder: {self.order.date.date()}'
        return f'{self.product.name}, of: {self.user.username}'

class Coupon(models.Model):
    name = models.CharField(max_length=100)
    discount = models.FloatField()
    quantity = models.IntegerField()
    dateEx = models.DateField()

    def __str__(self):
        return self.name


