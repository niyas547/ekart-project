from django.contrib import admin
from ekart.models import Category,Products,Carts,Review

# Register your models here.
admin.site.register(Category)
admin.site.register(Products)
admin.site.register(Carts)
admin.site.register(Review)
