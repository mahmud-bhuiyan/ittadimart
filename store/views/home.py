from django.shortcuts import render
from store.models.product import Product
from store.models.category import Category


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