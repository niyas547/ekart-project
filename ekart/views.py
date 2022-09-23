from django.shortcuts import render
from ekart.serializers import CategorySerializer,ProductSerializer,CartSerializer,UserSerializer,ReviewSerializer
from ekart.models import Category,Products,Carts,Review
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework import permissions
from rest_framework.decorators import action

# Create your views here.

class CategoryView(ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    #localhost:8000/ekart/category/1/add_produsts/
    @action(methods=["POST"],detail=True)
    def add_products(self,request,*args,**kwargs):
        cid=kwargs.get("pk")
        cat=Category.objects.get(id=cid)
        serializer=ProductSerializer(data=request.data,context={"category":cat})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    # permission_classes =[permissions.IsAuthenticatedOrReadOnly]
    @action(methods=["GET"],detail=True)
    def get_products(self,request,*args,**kwargs):
        cid=kwargs.get("pk")
        cat=Category.objects.get(id=cid)
        products=cat.products_set.all()
        serializer=ProductSerializer(products,many=True)
        return Response(data=serializer.data)

class ProductView(ViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    #localhost:8000/ekart/products/
    def list(self,request,*args,**kwargs):
        all_products=Products.objects.all()
        if "category" in request.query_params:
            all_products=all_products.filter(category=request.query_params.get("category"))
        serializer=ProductSerializer(all_products,many=True)
        return Response(data=serializer.data)


    #localhost:8000/ekart/products/1/
    def retrieve(self,request,*args,**kwargs):
        pid=kwargs.get("pk")
        product=Products.objects.get(id=pid)
        serializer=ProductSerializer(product,many=False)
        return Response(data=serializer.data)


    #localhost:8000/ekart/products/1/add_to_cart/
    @action(methods=["POST"],detail=True)
    def add_to_cart(self,request,*args,**kwargs):
        pid=kwargs.get("pk")
        product=Products.objects.get(id=pid)
        user=request.user
        serializer=CartSerializer(data=request.data,context={"product":product,"user":user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    # localhost:8000/ekart/products/1/add_review
    @action(methods=["POST"],detail=True)
    def add_review(self,request,*args,**kwargs):
        pid=kwargs.get("pk")
        product=Products.objects.get(id=pid)
        user=request.user
        serializer=ReviewSerializer(data=request.data,context={"product":product,"user":user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


class CartView(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializer
    queryset = Carts.objects.all()
    def get_queryset(self):
        return Carts.objects.filter(user=self.request.user)


class UsersView(ViewSet):
    def create(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)



