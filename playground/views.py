import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Value,F,Func
from django.db.models.aggregates import Count ,Max ,Min ,Avg ,Sum

from store.models import Cart, CartItem, Product,Customer,Order,OrderItem,Collection

# Create your views here.

def say_hello(request):
    
    new = CartItem()
    
    context = {"results":new}
    return render(request, 'playground/hallo.html',context)

    
    

def home(request):
  
    return render(request,'playground/home.html')
