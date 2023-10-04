from django.shortcuts import render, HttpResponse, redirect
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseServerError, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
import requests
from bs4 import BeautifulSoup
from django.template.defaultfilters import truncatewords
import json
import razorpay
import xhtml2pdf.pisa as pisa
from django.template.loader import get_template
from base.helpers import save_pdf
from io import BytesIO
import os


@login_required(login_url='login')
def HomePage(request):
    categories = Category.objects.all()
    context = {'products': Product.objects.all(), 'categories': categories}
    return render(request, 'home/home.html',  context)


def SignupPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        user_check = User.objects.filter(username=uname).exists()
        email_check = User.objects.filter(email=email).exists()

        if user_check:
            messages.success(request, 'Username is taken.')
            return redirect('signup')

        if email_check:
            messages.success(request, 'Email is taken.')
            return redirect('signup')

        if pass1 != pass2:
            messages.success(request, 'Your password and confirm password are not the same!!')
            return redirect('signup')

        else:
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user=my_user, auth_token=auth_token)
            profile_obj.save()
            send_mail_after_registration(email, auth_token)
            return redirect('token_send')
    return render(request, 'login/signup.html')


def success(request):
    return render(request, 'login/success.html')


def token_send(request):
    return render(request, 'login/token_send.html')


def LoginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, 'Username or Password is incorrect!!!')
            return redirect('login')
    return render(request, 'login/login.html')


def LogoutPage(request):
    logout(request)
    return redirect('login')


def error_page(request):
    return render(request, 'login/error.html')


def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                return redirect('login')
            profile_obj.is_verified = True
            profile_obj.save()
            return redirect('success')
        else:
            return redirect('error')
    except Exception as e:
        print(e)
        return redirect('/')


def send_mail_after_registration(email, token):
    subject = 'Your account needs to be verified'
    message = f'Hi click the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


def contact_us(request):
    if request.method == "POST":
        nameCon = request.POST.get('nameCon')
        emailCon = request.POST.get('emailCon')

        message = request.POST.get('message')
        contact_message = ContactUs(nameCon=nameCon, emailCon=emailCon, message=message)
        contact_message.save()
        messages.success(request, "Comment Successfully Submit")

        return redirect('/home')


def search_results(request):
    query = request.GET.get('query')

    # Check if the product exists in the database
    try:
        product = Product.objects.get(product_name__icontains=query)
        return redirect('get_product', slug=product.slug)
    except Product.DoesNotExist:
        pass

    # Product not found in the database, perform web scraping

    flipkart_url = "https://www.flipkart.com/search?q=" + query
    flipkart_r = requests.get(flipkart_url)
    flipkart_soup = BeautifulSoup(flipkart_r.text, "html.parser")

    results = []

    # Flipkart scraping
    flipkart_box = flipkart_soup.find("div", class_="_1YokD2 _3Mn1Gg")
    if flipkart_box:
        flipkart_images = flipkart_box.find_all("img", class_="_2r_T1I") or flipkart_box.find_all("img", class_="_396cs4") or flipkart_box.find_all("img", class_="CXW8mj")
        flipkart_names = flipkart_box.find_all("a", class_="IRpwTa") or flipkart_box.find_all("a", class_="s1Q9rs") or flipkart_box.find_all("div", class_="_4rR01T")
        flipkart_prices = flipkart_box.find_all("div", class_="_30jeq3") or flipkart_box.find_all("div", class_="_30jeq3") or flipkart_box.find_all("div", class_="_25b18c")
        flipkart_brands = flipkart_box.find_all("div", class_="_2WkVRV") or flipkart_box.find_all("a", class_="s1Q9rs") or flipkart_box.find_all("div", class_="_4rR01T")
        flipkart_link = flipkart_box.find_all("a", class_="_2rpwqI") or flipkart_box.find_all("a", class_="_1fQZEK")
        for image, name, price, brand, link in zip(flipkart_images, flipkart_names, flipkart_prices, flipkart_brands, flipkart_link):
            brand_words = brand.text.split()[:3]
            brand_name = ' '.join(brand_words)
            product_url = "https://www.flipkart.com" + link['href'] if link else ''
            product = {
                'image_link': image['src'],
                'product_name': name.text,
                'price': price.text.replace('.00', ''),
                'product_brand': brand.text,
                'product_url': product_url,
                'source': 'Flipkart'
            }
            results.append(product)

    context = {
        'results': results,
        'query': query,
    }

    return render(request, 'search/search_results.html', context)


def add_cart(request, product_id):
    if request.method == 'GET':
        quantity = request.GET.get('quantity', 1)
        images= request.GET.get  ('image_link')
        names =request.GET.get ('product_name')
        prices=request.GET.get  ('price')
        des = request.GET.get ('product_description')
        brands=request.GET.get ('product_brand')

        return render(request, 'search/search_cart.html')



def get_product(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        context = {'product': product}

        if request.GET.get('size'):
            size = request.GET.get('size')
            price = product.get_product_price_by_size(size)
            context['selected_size'] = size
            context['updated_price'] = price
            print(price)
            
        return render(request, 'product/product-des.html', context=context)

    except Product.DoesNotExist:
        return HttpResponseNotFound("Product not found")

    except Exception as e:
        print(e)
        return HttpResponseServerError("An error occurred")


def add_to_cart(request, uid):
    variant = request.GET.get('size')
    quantity = int(request.GET.get('quantity', 1))
    product = Product.objects.get(uid=uid)
    user = request.user
    cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)
    cart_item = CartItems.objects.create(cart=cart, product=product, quantity=quantity)

    if variant:
        size_variant = SizeVariant.objects.get(size_name=variant)
        cart_item.size_variant = size_variant
        cart_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def remove_cart(request, cart_item_uid):
    try:
        cart_item = CartItems.objects.get(uid=cart_item_uid)
        cart_item.delete()
    except Exception as e:
        print(e)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def product_description(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {'product': product}
    return render(request, 'product/product_desc.html', context)

def product_list(request, category):
    selected_category = Category.objects.get(slug=category)
    products = Product.objects.filter(category=selected_category)
    return render(request, 'product/product_list.html', {'products': products})


from django.contrib.auth.decorators import login_required
from django.conf import settings


@login_required
def cart(request):
    cart = None
    try:
        cart = Cart.objects.get(user=request.user, is_paid=False)
    except Cart.DoesNotExist:
        pass

    cart_items = cart.cart_items.all() if cart else []
    total_price = cart.get_cart_total() if cart else 0
    total_items = cart_items.count() if cart else 0
    
    payment= None
    
    if cart:
        client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
        amount_in_paise = int(cart.get_cart_total() * 100)
        payment = client.order.create({'amount': amount_in_paise, 'currency': "INR", 'payment_capture': 1 })
        cart.razor_pay_order_id= payment['id']
        cart.save()
        
        
        print('*****')
        print (payment)
        print('*****')
        

    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_items': total_items,
        'payment': payment
    }
    return render(request, 'product/cart.html', context)


from django.template.loader import render_to_string

def save_pdf(params: dict):
    template = 'pdf/invoice.html'
    html = render_to_string(template, params)
    file_name = str(uuid.uuid4())

    if not os.path.exists(settings.MEDIA_ROOT):
        os.makedirs(settings.MEDIA_ROOT)

    file_path = os.path.join(settings.MEDIA_ROOT, f"{file_name}.pdf")

    with open(file_path, 'wb') as f:
        pisa.pisaDocument(BytesIO(html.encode("UTF-8")), f)

    return file_name, True


def payment_success(request):
    order_id = request.GET.get('order_id')
    cart = Cart.objects.get(razor_pay_order_id=order_id)
    cart.is_paid = True
    cart.save()

    # Generate the PDF invoice
    params = {
        'payment': {
            'id': cart.razor_pay_order_id,
            'amount': cart.get_cart_total(),
            'currency': 'INR',  # Update with your desired currency
            'name': cart.user.username,
            'description': 'Payment Invoice'
        }
    }
    file_name, success = save_pdf(params)

    if success:
        download_link = os.path.join(settings.MEDIA_URL, f"{file_name}.pdf")

        # Provide a message and options for download and returning to the home page
        message = "Payment successful. Invoice generated."
        context = {
            'message': message,
            'download_link': download_link
        }
        return render(request, 'pdf/successful.html', context)

    return HttpResponse('Payment Success')

# def import_products(request):
    if request.method == 'POST':
        form = ProductImportForm(request.POST, request.FILES)
        if form.is_valid():
            product_resource = ProductResource()
            dataset = Dataset()
            new_products = request.FILES['file']

            if not new_products.name.endswith('.xlsx'):
                messages.error(request, 'File format not supported. Please upload an Excel file.')
                return render(request, 'import.html', {'form': form})

            imported_data = dataset.load(new_products.read(), format='xlsx')
            result = product_resource.import_data(dataset, dry_run=True)  # Perform a dry run to check for errors

            if not result.has_errors():
                product_resource.import_data(dataset, dry_run=False)  # Perform the actual import
                messages.success(request, 'Products imported successfully.')
            else:
                messages.error(request, 'Error importing products. Please check the file and try again.')
    else:
        form = ProductImportForm()

    return render(request, 'base/import.html', {'form': form})



# def import_categories(request):
    if request.method == 'POST':
        form = CategoryImportForm(request.POST, request.FILES)
        if form.is_valid():
            category_resource = CategoryResource()
            dataset = Dataset()
            new_categories = request.FILES['file']

            if not new_categories.name.endswith('.xlsx'):
                messages.error(request, 'File format not supported. Please upload an Excel file.')
                return render(request, 'import.html', {'form': form})

            imported_data = dataset.load(new_categories.read(), format='xlsx')
            result = category_resource.import_data(dataset, dry_run=True)  # Perform a dry run to check for errors

            if not result.has_errors():
                category_resource.import_data(dataset, dry_run=False)  # Perform the actual import
                messages.success(request, 'Categories imported successfully.')
            else:
                messages.error(request, 'Error importing categories. Please check the file and try again.')
    else:
        form = CategoryImportForm()

    return render(request, 'base/import.html', {'form': form})



# def collections(request):
    category = Category.objects.filter(status=0)
    context = {'category': category}
    return render (request, 'home.html', context)