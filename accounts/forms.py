from django.forms import ModelForm
from django import forms
from .models import Order, Customer, Product
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomerForm(ModelForm):
    class Meta: 
        model = Customer
        fields = '__all__'
        exclude = ['user']

class OrderForm(ModelForm):
    class Meta: 
        model = Order
        # fields = ['customer']
        fields = '__all__'


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

# class LoginUserForm