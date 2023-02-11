# from django.http import HttpResponse
from django.shortcuts import render
from django.db import IntegrityError
from .forms import BookingForm
from .models import Menu
from django.core import serializers as ser
from .models import Booking
from datetime import datetime
import json
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework import generics
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from .serializers import *
from django.contrib.auth import authenticate,login as dj_login,logout
# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['pass']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            dj_login(request,user)
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request,'login.html',{

                'message':'Error,this user does not exist'
                
            })
    return render(request,'login.html')
def register(request):
    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['pass']
        cpassword = request.POST['cpass']
        if password != cpassword:
            return render(request,'register.html',{'message':"Passwords didn't match"})
        try:
            user = User.objects.create_user(username=username,password=password)
        except IntegrityError:
            return render(request,'register.html',{'message':"User already exists"})
        dj_login(request,user)
        return HttpResponseRedirect(reverse('home'))
    return render(request,'register.html')

def logingout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def reservations(request):
    date = request.GET.get('date',datetime.today().date())
    bookings = Booking.objects.all()
    booking_json = ser.serialize('json', bookings)
    return render(request, 'bookings.html',{"bookings":booking_json})

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'book.html', context)

# Add your code here to create new views
def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})


def display_menu_item(request, pk=None): 
    if pk: 
        menu_item = Menu.objects.get(pk=pk) 
    else: 
        menu_item = "" 
    return render(request, 'menu_item.html', {"menu_item": menu_item}) 

@csrf_exempt
def bookings(request):
    if request.method == 'POST':
        data = json.load(request)
        print(data)
        exist = Booking.objects.filter(reservation_date=data['reservation_date']).filter(
            reservation_slot=data['reservation_slot']).exists()
        if exist==False:
            booking = Booking(
                first_name=data['first_name'],
                reservation_date=data['reservation_date'],
                reservation_slot=data['reservation_slot'],
            )
            booking.save()
        else:
            return HttpResponse("{'error':1}", content_type='application/json')
    
    date = request.GET.get('date',datetime.today().date())

    bookings = Booking.objects.all().filter(reservation_date=date)
    booking_json = serializers.serialize('json', bookings)

    return HttpResponse(booking_json, content_type='application/json')

# API Views
# Don't change anything, i'm serious


class BookingAPI(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    def get_queryset(self):
        queryset = Booking.objects.all()
        if 'reservation_date' in self.request.query_params:
            queryset = Booking.objects.filter(reservation_date=self.request.query_params['reservation_date'])
        return queryset
    
    
class BookingItemAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    lookup_field = 'id'
    serializer_class = BookingSerializer
    

class MenuAPI(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
 
    
class MenuItemAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    lookup_field = 'id'
    serializer_class = MenuSerializer