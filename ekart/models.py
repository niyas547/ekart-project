from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator


# Create your models here.

class Category(models.Model):
    category_name=models.CharField(max_length=120)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.category_name

class Products(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    product_name=models.CharField(max_length=120,unique=True)
    price=models.PositiveIntegerField()
    image=models.ImageField(upload_to="product_images",null=True)
    description=models.CharField(max_length=300)

    def __str__(self):
        return self.product_name

class Carts(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    added_date=models.DateTimeField(auto_now_add=True)
    options=(
        ("in-cart","in-cart"),
        ("order-placed","order-placed"),
        ("cancelled","cancelled")
    )
    status=models.CharField(max_length=120,choices=options,default="in-cart")

class Review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    comment=models.CharField(max_length=200)
    rating=models.FloatField(default=3.5,null=True)



    class Meta:
        unique_together=("user","product")


#validators=[MinValueValidator(1),MaxValueValidator(5)],null=True