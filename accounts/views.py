from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import *
from django.contrib.auth.models import Group
from .forms import OrderForm, CreateUserForm, CustomerForm, ProductForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only

# Create your views here.


@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.info(request, 'Account does not exist')
            # print(messages)
    return render(request, 'accounts/login.html')


def logoutPage(request):
    logout(request)
    return redirect('home')
    
@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # username = form.cleaned_data.get('username')

            messages.success(request, f'Account was created for {{user}}')
            return redirect('login')

    context = {'form': form}
    
    return render(request, 'accounts/register.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def home(request):
    orders = Order.objects.all().order_by('id')
    customers = Customer.objects.all()
    delivered = orders.filter(status="Delivered")
    pending = orders.filter(status="Pending")

    context = {'orders': orders, 'customers': customers, 'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/dashboard.html', context)


def products(request):

    products = Product.objects.all()

    return render(request, 'accounts/products.html', {'products': products})

def create_product(request):

    form = ProductForm()
    context = {'form': form}

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save
            return redirect('products')

    return render(request, 'accounts/create_product.html', context)

    


@login_required(login_url='login')
def customer(request, pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer, 'orders': orders, 'myFilter': myFilter}

    return render(request, 'accounts/customer.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def profile(request):

    return render(request, 'accounts/profile.html')

@login_required(login_url='login')
def createOrder(request, pk):

    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('customer', pk)


    context = {'formset': formset}

    return render(request, 'accounts/order_form.html',  context)

@login_required(login_url='login')
def updateOrder(request, pk):

    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}


    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
def deleteOrder(request, pk):

    order = Order.objects.get(id=pk)

    if request.method == "POST":
        order.delete()
        return redirect('home')

    context = {'item': order}

    return render(request, 'accounts/delete_order.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    context = {'form': form}

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'accounts/account_settings.html', context)