from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, customized_role
from django.contrib.auth.models import Group


# Create your views here.
@login_required(login_url='login')
@customized_role
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_orders = orders.count()
    orders_delivered = orders.filter(status='Delivered').count()
    orders_pending = orders.filter(status='Pending').count()
    orders_ofd = orders.filter(status='Out for Delivery').count()
    context = {
        'orders': orders,
        'customers': customers,
        'total_orders': total_orders,
        'orders_delivered': orders_delivered,
        'orders_pending': orders_pending,
        'orders_ofd': orders_ofd
    }
    return render(request, 'index.html', context)


@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            # group = Group.objects.get(name='customer')
            # user.groups.add(group)

            # Customer.objects.create(
            #     user=user,
            #     name=user.username,
            # )

            messages.success(request, "Account was created for" + username)

            return redirect('login')
    context = {
        'form': form
    }
    return render(request, 'register.html', context)


@unauthenticated_user
def logIn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Credential's Invalid")
    context = {}
    return render(request, 'login.html', context)


@login_required(login_url='login')
def logOut(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def profile(request):
    orders = request.user.customer.order_set.all()
    # customer_profile = request.user.objects.customer.get()
    total_orders = orders.count()
    print(total_orders)
    orders_delivered = orders.filter(status='Delivered').count()
    orders_pending = orders.filter(status='Pending').count()
    orders_ofd = orders.filter(status='Out for Delivery').count()
    context = {
        'orders': orders, 'total_orders': total_orders, 'orders_delivered': orders_delivered,
        'orders_pending': orders_pending, 'orders_ofd': orders_ofd
    }
    return render(request, 'profile.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def account_settings(request):
    customer_profile = request.user.customer
    form = CustomerForm(instance=customer_profile)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    context = {
        'form': form
    }
    return render(request, 'settings.html', context)


@login_required(login_url='login')

def products(request):
    product = Product.objects.all()
    return render(request, 'product.html', {'product': product})


@login_required(login_url='login')
def customer(request, id):
    customers = Customer.objects.get(id=id)
    customer_orders = customers.order_set.all()
    order_count = customer_orders.count()

    myFilter = OrderFilter(request.GET, queryset=customer_orders)
    customer_orders = myFilter.qs

    context = {
        'customers': customers,
        'customer_orders': customer_orders,
        'order_count': order_count, 'myFilter': myFilter,
    }
    return render(request, 'customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_order(request, id):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=3)
    customer_order = Customer.objects.get(id=id)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer_order)
    # form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer_order)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'form': formset}
    return render(request, 'create_order.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_order(request, id):
    order = Order.objects.get(id=id)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {
        'form': form
    }
    return render(request, 'create_order.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, id):
    order = Order.objects.get(id=id)
    if request.method == 'POST':
        order.delete()
        return redirect('home')
    context = {
        'order': order
    }
    return render(request, 'delete_order.html', context)
