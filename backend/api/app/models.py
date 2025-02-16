from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.ImageField(upload_to='images/category/')

    def __str__(self):
        return self.name
    
class Products(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, default='No description available')
    price = models.FloatField()
    discount = models.FloatField()
    image_url = models.ImageField(upload_to='images/products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Delevry(models.Model):
    # i will modify this model like a user model

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

class Address(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    lang = models.FloatField()
    lat = models.FloatField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name, 'of', self.user
    
class Orders(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    delivery = models.ForeignKey(Delevry, on_delete=models.CASCADE)
    total_price = models.FloatField()
    quantity = models.IntegerField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    status = models.TextChoices(['pending','delivered','3','4'])
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user
    


class Cart(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

class Coupon(models.Model):
    name = models.CharField(max_length=100)
    discount = models.FloatField()
    quantity = models.IntegerField()
    dateEx = models.DateField()

    def __str__(self):
        return self.name


