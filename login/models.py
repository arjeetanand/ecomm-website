from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.conf import settings
from base.models import BaseModel


class Category(BaseModel):
    category_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category_image = models.ImageField(upload_to="categories", blank=True)
    image_link = models.URLField(default='your_default_image_link')
    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "Categories"


class ColorVariant(BaseModel):
    color_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.color_name

    class Meta:
        verbose_name_plural = "Color Variants"


class SizeVariant(BaseModel):
    size_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.size_name

    class Meta:
        verbose_name_plural = "Size Variants"


class Product(BaseModel):
    product_name = models.CharField(max_length=100, unique=True)
    product_brand = models.CharField(max_length=100, null=True, blank=True, default='Unknown Brand')
    slug = models.SlugField(unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    price = models.IntegerField()
    product_description = models.TextField()
    color_variant = models.ManyToManyField(ColorVariant, blank=True)
    size_variant = models.ManyToManyField(SizeVariant, blank=True)
    image_link = models.URLField(default='your_default_image_link')
    # product_image = models.ImageField(upload_to="categories", blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name

    def get_product_price_by_size(self, size):
        return self.price + SizeVariant.objects.get(size_name=size).price

    class Meta:
        verbose_name_plural = "Products"


# class ProductImage(BaseModel):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")
#     image = models.ImageField(upload_to="products")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def get_cart_count(self):
        return self.user.carts.filter(is_paid=False).count()
    
    
class ContactUs(models.Model):
    nameCon = models.CharField(max_length=255, blank=True, null=True)
    emailCon = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nameCon


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    is_paid = models.BooleanField(default=False)
    razor_pay_order_id = models.CharField(max_length=100, null=True ,blank= True)
    razor_pay_payment_id = models.CharField(max_length=100, null=True ,blank= True)
    razor_pay_payment_signature = models.CharField(max_length=100, null=True ,blank= True)

    # Rest of your model code...
    
    def get_cart_total (self):
        cart_items = self.cart_items.all()
        price = []
        for cart_item in cart_items:
            price.append(cart_item.product.price)
            if cart_item.color_variant:
                color_variant_price = cart_item.color_variant.price
                price.append(color_variant_price)
            if cart_item.size_variant:
                size_variant_price = cart_item.size_variant.price
                price.append (size_variant_price)
                
        
        # if self.coupon:
        #     print(self.coupon.minimum_amount)
        #     print(sum(price))
        #     if self.coupon.minimum_amount < sum(price):
        #         return sum(price) - self.coupon.discount_price
        
        # print (price)
        return sum(price)
    class Meta:
        verbose_name_plural = "Carts"


class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    color_variant = models.ForeignKey(ColorVariant, on_delete=models.SET_NULL, null=True, blank=True)
    size_variant = models.ForeignKey(SizeVariant, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return f"{self.product} - {self.quantity}"

    def get_product_price(self):
        price = [self.product.price]
        
        if self.color_variant:
            color_variant_price = self.color_variant.price
            price.append(color_variant_price)
        if self.size_variant:
            size_variant_price = self.size_variant.price
            price.append(size_variant_price)
        return sum(price)

    class Meta:
        verbose_name_plural = "Cart Items"
