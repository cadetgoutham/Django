from django.shortcuts import redirect, render
import requests
from .models import Product

# Create your views here.    
    

def product_list(request):
    products = Product.objects.all()
    if not products:
        response = requests.get('https://fakestoreapi.com/products')
        items = response.json()
        for item in items:
            print(f"Adding product: {item.get('rating', {}).get('rate', 0)}")
            Product.objects.get_or_create(
                name=item.get('title'),
                defaults={ 
                    'price': item.get('price'), 
                    'description': item.get('description'),
                    'category': item.get('category'),
                    'image': item.get('image'),
                    'rating': item.get('rating', {}).get('rate', 0.0),
                    'rating_count': item.get('rating', {}).get('count', 0),
                }
            )
        db_items = Product.objects.all()
        return render(request, 'ecommerce/home.html', {'items': db_items})
    else:
        print(f"Products already in database: {products[0].id}")
        data = []
        cart = request.session.get('cart', {})
        cart_count = sum(cart.values())
        for product in products:
            data.append({
                'id': product.id,
                'name': product.name,
                'price': str(product.price),
                'description': product.description,
                'category': product.category,
                'image': product.image,
                'rating': product.rating,
                'rating_count': product.rating_count,
                'qty_in_cart': cart.get(str(product.id), 0),
            })
        return render(request, 'ecommerce/home.html', {'items': data, 'count': cart_count, 'cart': cart})

def product_detail(request, pk):
    try:
        product = Product.objects.get(id=pk)
        cart = request.session.get('cart', {})
        product_cart_count =  cart.get(str(product.id))
        cart_count = sum(cart.values()) | 0
        data = {
            'id': product.id,
            'name': product.name,
            'price': str(product.price),
            'description': product.description,
            'category': product.category,
            'image': product.image,
            'rating': product.rating,
            'rating_count': product.rating_count,
        }
        return  render(request, 'ecommerce/Product.html', 
                       {
                           'product': data, 
                           'count': cart_count, 
                           'product_cart_count': product_cart_count
                        })
    except Product.DoesNotExist:
        return redirect('ecommerce_home')
    
def product_category(request, category):
    products = Product.objects.filter(category=category)
    data = []
    cart = request.session.get('cart', {})
    for product in products:
        data.append({
            'id': product.id,
            'name': product.name,
            'price': str(product.price),
            'description': product.description,
            'category': product.category,
            'image': product.image,
            'rating': product.rating,
            'rating_count': product.rating_count,
            'qty_in_cart': cart.get(str(product.id), 0),
        })
    cart_count = sum(cart.values())
    product_cart_count =  cart.get(str(product.id))
    return render(request, 'ecommerce/Category.html', 
                  {
                      'items': data, 
                      'category': category, 
                      'count': cart_count, 
                      'cart': cart
                })

def add_to_cart(request, pk, url):
    cart = request.session.get('cart', {})

    # Add or increment the product quantity
    product_id_str = str(pk) # Session keys must be strings
    if product_id_str in cart:
        cart[product_id_str] += 1
    else:
        cart[product_id_str] = 1

    # Save the cart back to the session
    request.session['cart'] = cart
    if url == 'product_detail':
        return redirect(url, pk=pk)
    if url == 'product_category':
        product = Product.objects.get(pk=pk)
        return redirect(url, category=product.category)
    return redirect(url)

def decrement_cart_count(request, pk, url):
    cart = request.session.get('cart', {})
    print(f"Current cart before decrement: {url}")

    # Remove or decrement the product quantity
    product_id_str = str(pk) # Session keys must be strings
    if product_id_str in cart:
        if cart[product_id_str] > 1:
            cart[product_id_str] -= 1
        else:
            del cart[product_id_str]

    # Save the cart back to the session
    request.session['cart'] = cart
    if url == 'product_detail':
        return redirect(url, pk=pk)
    if url == 'product_category':
        product = Product.objects.get(pk=pk)
        return redirect(url, category=product.category)
    return redirect(url)

def remove_from_cart(request, pk, url):
    cart = request.session.get('cart', {})
    product_id_str = str(pk) # Session keys must be strings
    if product_id_str in cart:
        del cart[product_id_str]
    request.session['cart'] = cart
    if url == 'product_detail':
        return redirect(url, pk=pk)
    if url == 'product_category':
        product = Product.objects.get(pk=pk)
        return redirect(url, category=product.category)
    return redirect(url)

def clear_cart(request):
    request.session['cart'] = {}
    return redirect('ecommerce_home')

def cart(request):
    cart = request.session.get('cart', {})
    items = []
    cart_total = 0
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            cart_total += product.price * quantity
            items.append({
                'id': product.id,
                'name': product.name,
                'price': str(product.price),
                'description': product.description,
                'category': product.category,
                'image': product.image,
                'rating': product.rating,
                'rating_count': product.rating_count,
                'quantity': quantity,
                'total_price': str(product.price * quantity),
            })
        except Product.DoesNotExist:
            continue
    cart_count = sum(item['quantity'] for item in items)
    return render(request, 'ecommerce/Cart.html', 
                  {
                      'items': items, 
                      'count': cart_count, 
                      'cart': cart,
                      'cart_total': cart_total
                  })