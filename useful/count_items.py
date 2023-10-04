import os
import django

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopping.settings')

# Initialize Django
django.setup()

from login.models import Product,Category,ColorVariant,SizeVariant

def count_items():
    product_count = Product.objects.count()
    Category_count = Category.objects.count()
    ColorVariant_count = ColorVariant.objects.count()
    SizeVariant_count = SizeVariant.objects.count()
    # Category, ColorVariant, or SizeVariant.
    print("Number of created products:", product_count)
    print("Number of created Category:", Category_count)
    print("Number of created ColorVariant:", ColorVariant_count)
    print("Number of created SizeVariant:", SizeVariant_count)

# Call the function to get the count of items
count_items()
