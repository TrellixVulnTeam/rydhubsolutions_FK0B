from django.shortcuts import render
from django.views import View
from products.models import Category, Supplier, Product, ProductImage
import os
from rest_framework import viewsets
from .serializers import CategorySerializer, SupplierSerializer, ProductSerializer, ProductImageSerializer
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse
from cart.models import Cart
from cart.utils.cart_management import CartManager
from products.utils.model_string_search import search_for_something
import urllib

class BaseLoader(View):
    # load main page with products based on selected category
    def get(self, request, filter = ''):
        self.all_categories = Category.update_sub_category_lists()
        self.categories = Category.find_main_categories(self.all_categories)

        # here we use the filter to load the products accordingly!
        if filter != '':
            try:
                self.category_from_filter = Category.objects.get(name = filter)
            except:
                return HttpResponseNotFound("category not available")
            self.list_of_all_categories_from_filter = Category.get_all_sub_categories(self.category_from_filter)
            self.list_of_all_categories_from_filter.append(self.category_from_filter)
            self.all_products = Product.get_products_from_list_of_categories(self.list_of_all_categories_from_filter)
        else:
            self.all_products = Product.get_all_products()

        # update the descripton of the product
        for product in self.all_products:
            if len(product.description) > 80:
                product.description = product.description[:80] + '...' 

        #now we find all the images we need for each product
        self.all_product_images = []
        for product in self.all_products:
            img = list(ProductImage.find_all_product_images(product.id))
            self.all_product_images += img

        # here we zip the product data with another list that has values to help the template determine when it should start a new card-deck as apposed to card
        card_deck_update_check = []
        i= 0
        for product in self.all_products:
            if i==0:
                card_deck_update_check.append('first')
            elif i%3:
                card_deck_update_check.append(False)
            else:
                card_deck_update_check.append(True)
            i += 1
        products_and_carddeck_checker = zip(self.all_products, card_deck_update_check)

        if filter == '':
            self.featured_products = Product.objects.filter(featured=True)

            self.featured_product_images = []
            for featured_product in self.featured_products:
                img = list(ProductImage.find_all_product_images(featured_product.id))
                self.featured_product_images += img
        # this should be to load the homepage, so give featured products and catalog data                                                                                                                                                                                              featured_products
            return render(request, 'products/home.html', {'main_categories':self.categories, 'all_categories':self.all_categories, 'products':self.all_products, 'products_and_carddeck_checker':products_and_carddeck_checker, 'product_images':self.all_product_images, 'empty_list':[], 'featured_products':self.featured_products, 'featured_product_images':self.featured_product_images })
        return render(request, 'products/home.html', {'main_categories':self.categories, 'all_categories':self.all_categories, 'products':self.all_products, 'products_and_carddeck_checker':products_and_carddeck_checker, 'product_images':self.all_product_images, 'empty_list':[] })




def product_page(request, product_id):
    # get cart data
    cart_manager = CartManager(request)
    # creating the urls needed by the template to make its request to the api
    urls_cart = request.build_absolute_uri('/api/cart/' + urllib.parse.quote(str(cart_manager.cart.id)) + '/')
    urls_product = request.build_absolute_uri('/api/products/' + urllib.parse.quote(str(product_id)) + '/')
    
    if request.user.is_authenticated:
        username = request.user.get_username()
    else:
        username = ''

    #find product and give it to template
    main_product = Product.objects.get(id = product_id)
    main_image = ProductImage.find_main_product_image(product_id)
    other_images = ProductImage.find_product_images(product_id)


    return render(request, 'products/product.html', {'product':main_product, 'main_image':main_image, 'other_images':other_images, 'cart':cart_manager.cart, 'urls_cart':urls_cart, 'urls_product':urls_product, 'username':username})


def product_search(request):
    all_categories = Category.update_sub_category_lists()
    categories = Category.find_main_categories(all_categories)

    # this function here uses whats in the search bar and uses that string to find all products related to it, the search results are not ordered in anyway, its random, which should be changed
    found_products = search_for_something(request)

    if found_products:
        for product in found_products:
            if len(product.description) > 80:
                product.description = product.description[:80] + '...' 


    # here we zip the product data with another list that has values to help the template determine when it should start a new card-deck as apposed to card
    products_and_carddeck_checker = []
    if found_products:
        card_deck_update_check = []
        i= 0
        for product in found_products:
            if i==0:
                card_deck_update_check.append('first')
            elif i%3:
                card_deck_update_check.append(False)
            else:
                card_deck_update_check.append(True)
            i += 1
        products_and_carddeck_checker = zip(found_products, card_deck_update_check)


    all_product_images = []
    if found_products:
        for product in found_products:
            img = list(ProductImage.find_all_product_images(product.id))
            all_product_images += img
    
    search_string = request.GET['search_string']
    return render(request, 'products/home.html', {'main_categories':categories, 'all_categories':all_categories, 'products':found_products, 'products_and_carddeck_checker':products_and_carddeck_checker, 'product_images':all_product_images, 'empty_list':[], 'search_string':search_string })

















#these are for setting up the api for all the models using the django rest framework
class SupplierView(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductImageView(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer




# simple session read write api
class SessionAccess(View):
    def get(self, request):
        index = request.GET['index']
        if index in request.session:
            return HttpResponse(request.session[index])
        else:
            return HttpResponse(False)


    def post(self, request):
        index = request.POST['index']
        value = request.POST['value']
        request.session[index] = value
        return HttpResponse(request.session[index])




# api -> featured product + featured product images, title
# notinapi -> urll 'products:product_page'

#simple api request that takes in app name, path url name, and returns the full url, its like being able to do {{ url 'appName:urlName' 'variable'}}
def get_url(request):
    app_and_url_name = request.GET['app_and_url_name']
    if request.GET['url_arg']:
        url_arg =  request.GET['url_arg']
        url = reverse(app_and_url_name, args=[url_arg])
    else:
        url = reverse(app_and_url_name)
    return HttpResponse(url)

