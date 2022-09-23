from django.urls import path


from rest_framework.routers import DefaultRouter
from ekart import views
router=DefaultRouter()
router.register("categories",views.CategoryView,basename="category")
router.register("products",views.ProductView,basename="products")
router.register("carts",views.CartView,basename="carts")
router.register("accounts/signup",views.UsersView,basename="ekart_users")

urlpatterns =[


]+router.urls





