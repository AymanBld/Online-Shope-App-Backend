from django.db import models

# Create your models here.

class Products(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, default='No description available')
    price = models.FloatField()
    discount = models.FloatField()
    image_url = models.ImageField(upload_to='images/products/')
    category = models.OneToOneField('category', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class category(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.ImageField(upload_to='images/category/')

    def __str__(self):
        return self.name
    
class Orders(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    delivery = models.BooleanField(default=False)
    total_price = models.FloatField()
    quantity = models.IntegerField()
    address = models.CharField(max_length=1000)
    status = models.CharField(max_length=100, default='Pending')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name
    
class address(models.Model):
    address = models.CharField(max_length=1000)
    phone = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.email

class Cart(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.FloatField()
    address = models.CharField(max_length=1000)
    phone = models.CharField(max_length=100)
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

class coupon(models.Model):
    code = models.CharField(max_length=100)
    discount = models.FloatField()

    def __str__(self):
        return self.code

class delevry(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()

    def __str__(self):
        return self.name
