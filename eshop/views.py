from .models import Category, Product, Cart, CartItem
from .forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


def index(request):
    return render(request, 'index.html')


def products(request, category_slug = None):
    categoryID = None
    categories = Category.objects.all()
    products = Product.objects.filter(available = True)
    query = request.GET.get('query')
    sort = request.GET.get('select')
    print(sort)

    if query:
        products = products.filter(Q(name__contains = query))
    else:
        if sort == 'asc':
            products = products.order_by('price')
        elif sort == 'desc':
            products = products.order_by('-price')
        if category_slug:
            categoryID = get_object_or_404(Category, slug = category_slug)
            products = products.filter(categoryID = categoryID)

    return render(request, 'catalog.html', {
        'categoryID': categoryID,
        'categories': categories,
        'products': products,
        'query': query,
        'sort': sort
    })


def product(request, id, slug):
    product = get_object_or_404(Product, id = id, slug = slug, available = True)

    return render(request, 'product.html', { 'product': product })


def cart(request):
    cartID = request.session.get('cartID')
    cart = None

    if cartID:
        cart = get_object_or_404(Cart, id = cartID)
    if not cart or not cart.cart_items.exists():
        cart = None

    return render(request, 'cart.html', { 'cart': cart })


@require_POST
def cart_add(request, productID):
    cartID = request.session.get('cartID')

    if cartID:
        try:
            cart = Cart.objects.get(id = cartID)
        except Cart.DoesNotExist:
            cart = Cart.objects.create()
    else:
        cart = Cart.objects.create()
        request.session['cartID'] = cart.id

    product = get_object_or_404(Product, id = productID)

    cart_item, created = CartItem.objects.get_or_create(cartID = cart, productID = product)

    if not created:
        cart_item.quantity += 1

    cart_item.save()

    answer = { 'success': True }

    return JsonResponse(answer)


def cart_append(request, productID):
    cartID = request.session.get('cartID')
    cart = get_object_or_404(Cart, id = cartID)
    item = get_object_or_404(CartItem, id = productID, cartID = cart)
    item.quantity += 1
    item.save()

    return redirect('cart')


def cart_delete(request, productID):
    cartID = request.session.get('cartID')
    cart = get_object_or_404(Cart, id = cartID)
    item = get_object_or_404(CartItem, id = productID, cartID = cart)
    item.quantity -= 1
    
    if item.quantity == 0:
        item.delete()
    else:
        item.save()

    return redirect('cart')


@login_required(login_url = 'authorization')
def user(request):
    if request.user.is_authenticated:
        user = request.user
        orders = Order.objects.filter(clientID = request.user)
        order_items = OrderItem.objects.all()

        return render(request, 'orders.html', { 'user': user, 'orders': orders, 'order_items': order_items })
    else:
        return redirect('authorization')


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
           
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('index')
        else:
            messages.success(request, ('При регистрации возникла ошибка!'))
            return render(request, 'registration.html')
    else:
        form = RegistrationForm()
        return render(request, 'registration.html', { 'form': form })


def authorization(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('user')
        else:
            messages.success(request, ('Вы ввели неверный логин или пароль!'))
            return redirect('authorization')
    else: 
        return render(request, 'login.html')
    

def reset(request): 
    user = User.objects.get(username = request.user)

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            old_password = request.POST.get("old_password")
            new_password1 = request.POST.get("new_password1")

            if user.check_password(old_password):
                user.set_password(new_password1)
                user.save()
                update_session_auth_hash(request, user)
                return redirect('user')
            else:
                messages.success(request, 'Старый пароль введен неверно!')
                return redirect('reset') 
        else:
            messages.success(request, 'При обновлении пароля произошла ошибка!')
            return redirect('reset') 
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'reset.html', {'form': form, 'user': user})


def exit(request):
    logout(request)
    return redirect('index')


@login_required(login_url = "authorization")
def change(request):
    user = request.user
    form = UpdateForm(request.POST or None, instance = user)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            login(request, user)
            return redirect('user')
        else:
            messages.success(request, ('При обновлении информации возникла ошибка!'))
            return render(request, 'change.html', { 'user': user, 'form': form })
    else:
        return render(request, 'change.html', { 'user': user, 'form': form })


@login_required(login_url = 'authorization')
def create_order(request):
    cart = None
    cartID = request.session.get('cartID')
    user = request.user

    if cartID:
        cart = Cart.objects.get(id = cartID)

        if not cart or not cart.cart_items.exists():
            return redirect('cart')
        
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit = False)
            order.clientID = user
            order.save()

            for item in cart.cart_items.all():
                OrderItem.objects.create(
                    orderID = order,
                    productID = item.productID,
                    quantity = item.quantity
                )
            cart.delete()
            del request.session['cartID']
            return redirect('confirm_order', order.id)
        else:
            return redirect('create_order')
    else:
        form = OrderForm()
        return render(request, 'create_order.html', {
            'cart': cart,
            'form': form,
            'customer': user,
        })


@login_required(login_url = 'authorization')
def confirm_order(request, orderID):
    order = get_object_or_404(Order, id = orderID)
    return render(request, 'confirm_order.html', { 'order': order })