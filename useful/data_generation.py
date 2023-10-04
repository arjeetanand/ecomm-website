import os
import django

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopping.settings')

# Configure Django
django.setup()

from faker import Faker
from django.utils.text import slugify
import random
import string
import requests
from django.core.files.base import ContentFile
from google_images_search import GoogleImagesSearch

from login.models import Category, ColorVariant, SizeVariant, Product

fake = Faker()

# Set up Google Images Search API
google_search = GoogleImagesSearch('AIzaSyAtXN2oGQKP-ojRqdmm4cb5zIxw3Tj4M7s', 'f6c227c5d7bcc4d3a')
# Generate categories
categories = []
for _ in range(5):
    category_name = fake.word()
    slug = slugify(category_name) + "-" + ''.join(random.choices(string.ascii_lowercase, k=5))
    print(f"Creating category: {category_name}")

    # Use Google Images Search to get image URL based on category name
    google_search.search({'q': category_name, 'num': 1})
    image_url = google_search.results()[0].url

    category = Category.objects.create(
        category_name=category_name,
        slug=slug,
        image_link=image_url,)
    # category.category_image.save(f"{category_name}.jpg", ContentFile(requests.get(image_url).content), save=True)

    categories.append(category)
    print(f"Created category: {category.category_name}")

# Generate products
for _ in range(10):
    category = random.choice(categories)
    product_name = fake.word()
    print(f"Creating product: {product_name}")

    # Use Google Images Search to get image URL based on product name
    google_search.search({'q': product_name, 'num': 1})
    image_url = google_search.results()[0].url

    product = Product.objects.create(
        product_name=product_name,
        product_brand=fake.company(),
        category=category,
        price=random.randint(10, 100),
        product_description=fake.paragraph(),
        image_link=image_url,
    )

    # Download and save the product image
    # product_image = requests.get(image_url).content
    # product_image_name = f"{product_name}.jpg"
    # product.product_image.save(product_image_name, ContentFile(product_image), save=True)

    # Generate color variants for each product
    for _ in range(random.randint(1, 5)):
        color_variant = ColorVariant.objects.create(
            color_name=fake.color_name(),
            price=random.randint(1, 10),
        )
        product.color_variant.add(color_variant)

    # Generate size variants for each product
    for _ in range(random.randint(1, 3)):
        size_variant = SizeVariant.objects.create(
            size_name=fake.random_element(['S', 'M', 'L']),
            price=random.randint(1, 5),
        )
        product.size_variant.add(size_variant)

    print(f"Created product: {product.product_name}")

print("Data generation completed.")

# <script src="https://www.googleapis.com/customsearch/v1?key=YOUR-KEY&cx=017576662512468239146:omuauf_lfve&q=cars&callback=hndlr">

# https://cse.google.com/cse?cx=f6c227c5d7bcc4d3a
# <script async src="https://cse.google.com/cse.js?cx=f6c227c5d7bcc4d3a"></script><div class="gcse-search"></div>