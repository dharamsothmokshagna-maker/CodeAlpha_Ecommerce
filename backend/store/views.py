from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Product, Cart, Order


def home(request):
    products = Product.objects.all()
    return render(request, "index.html", {"products": products})


def product(request):
    return render(request, "product.html")


def cart(request):
    if not request.user.is_authenticated:
        return redirect("/login/")

    cart_items = Cart.objects.filter(user=request.user)

    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity

    return render(request, "cart.html", {
        "cart_items": cart_items,
        "total": total,
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")

    return render(request, "login.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect("/login/")

    return render(request, "register.html")


def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)
        Cart.objects.create(user=request.user, product=product)
        return redirect("/cart/")
    return redirect("/login/")


def checkout(request):
    if not request.user.is_authenticated:
        return redirect("/login/")

    cart_items = Cart.objects.filter(user=request.user)

    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity

    Order.objects.create(
        user=request.user,
        total=total
    )

    cart_items.delete()

    return render(request, "success.html")