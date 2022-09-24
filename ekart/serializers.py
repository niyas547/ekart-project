from rest_framework import serializers
from ekart.models import Category,Products,Carts,Review
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    is_active=serializers.BooleanField(read_only=True)
    class Meta():
        model=Category
        fields="__all__"

class ProductSerializer(serializers.ModelSerializer):
    category=serializers.CharField(read_only=True)
    class Meta:
        model=Products
        fields="__all__"

    def validate_price(self,value):
        if value not in range(20,200000):
            raise serializers.ValidationError("invalid price")
        return value

    def create(self, validated_data):
        category=self.context.get("category")
        return Products.objects.create(**validated_data,category=category)

class CartSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    product=ProductSerializer(read_only=True)
    created_date=serializers.CharField(read_only=True)
    status=serializers.CharField(read_only=True)
    class Meta:
        model=Carts
        fields="__all__"

    def create(self, validated_data):
        user=self.context.get("user")
        product=self.context.get("product")
        return Carts.objects.create(**validated_data,user=user,product=product)

class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)                         #do not read password
    class Meta:
        model=User
        fields=["first_name","last_name","email","username","password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class ReviewSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    product=serializers.CharField(read_only=True)
    class Meta:
        model=Review
        fields="__all__"

    def create(self, validated_data):
        product=self.context.get("product")
        user=self.context.get("user")
        return Review.objects.create(**validated_data,user=user,product=product)