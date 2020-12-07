from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models.product import Product
from .models.category import Category
from .models.customer import Customer


# Create your views here.
def index(request):
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        products = Product.get_all_products()
    data = {
        'products': products,
        'categories': categories
    }
    return render(request, 'index.html', data)


def validateCustomer(customer):

    error_message = None

    if (not customer.first_name):
        error_message = "First Name Required!"
    elif len(customer.first_name) < 4:
        error_message = "First Name must be 4 char long or more"

    elif len(customer.last_name) < 4:
        error_message = "Last Name must be 4 char long or more"

    if (not customer.phone):
        error_message = "Phone Number Required!"
    elif len(customer.phone) < 11:
        error_message = "Phone Number must be 11 char long"

    elif len(customer.email) < 5:
        error_message = "Email must be 4 char long or more"

    elif len(customer.password) < 4:
        error_message = "Password must be 4 char long or more"

    elif customer.isExists():
        error_message = 'Email Already Registered!'

    return error_message


def registerUser(request):
        postData = request.POST
        first_name = postData.get('first_name')
        last_name = postData.get('last_name')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')

        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }

        error_message =None

        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            password=password
        )

        error_message = validateCustomer(customer)


        if not error_message:
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('home')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        return registerUser(request)

