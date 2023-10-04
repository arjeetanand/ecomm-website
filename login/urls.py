from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('home/', HomePage, name='home'),
    path('', HomePage, name='home'),
    path('signup/', SignupPage, name='signup'),
    path('login/', LoginPage, name='login'),
    path('logout/', LogoutPage, name='logout'),
    path('token_send/', token_send, name='token_send'),
    path('success/', success, name='success'),
    path('verify/<str:auth_token>/', verify, name='verify'),
    path('error/', error_page, name='error'),
    path('ContactUs/', contact_us, name='contact_us'),
    path('cart/', cart, name='cart'),
    path('product/<slug>/', get_product, name='get_product'),
    path('add-to-cart/<str:uid>/', add_to_cart, name='add_to_cart'),
    path('product/<slug:slug>/', product_description, name='product_description'),
    path('remove-cart/<str:cart_item_uid>/', remove_cart, name='remove_cart'),
    path('product-desc/<slug:slug>/', get_product, name='get_product'),
    path('products/<slug:category>/', product_list, name='product_list'),
    path('search-results/', search_results, name='search_results'),
    path('add-cart/', add_cart, name='add_cart'),
    path('payment_success/', payment_success, name= "payment_success"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # path('import/products/', views.import_products, name='import_products'),
    # path('import/categories/', views.import_categories, name='import_categories'),