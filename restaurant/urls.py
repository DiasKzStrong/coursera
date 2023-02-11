from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('login/',views.login,name='loginsite'),
    path('logout/',views.logingout,name='logoutsite'),
    path('register/',views.register,name='register'),
    path('about/', views.about, name="about"),
    path('book/', views.book, name="book"),
    path('reservations/', views.reservations, name="reservations"),
    path('menu/', views.menu, name="menu"),
    path('menu_item/<int:pk>/', views.display_menu_item, name="menu_item"),  
    path('bookings', views.bookings, name='bookings'), 
    path('api/bookings',views.BookingAPI.as_view(),name='bookingapi'),
    path('api/bookings/<int:id>',views.BookingItemAPI.as_view(),name='bookingitemapi'),    
    path('api/menu',views.MenuAPI.as_view(),name='menuapi'),
    path('api/menu/<int:id>',views.MenuItemAPI.as_view(),name='menuitemapi')
]