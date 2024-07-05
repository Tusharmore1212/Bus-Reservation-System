"""
URL configuration for bus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('home/',views.home,name='home'),
    path('register/',views.reg),
    path('addbus/',views.addbus,name='addbus'),
    path('del_res/<int:id>/',views.delete_res,name='del_res'),
    path('bookticket/',views.book_ticket,name='bookticket'),
    path('search_bus/',views.search_bus,name='search_bus'),
    path('manage_bus/',views.manage_bus,name='manage_bus'),
    path('doupdatebus/<int:id>/',views.doupdatebus,name='doupdatebus'),
    path('login/',views.login.as_view(),name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user_dashboard/',views.user_dashboard,name='user_dashboard'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('manage_user/',views.manage_user,name='manage_user'),
    path('delete/<int:id>/',views.delete,name='delete'),
    path('deletebus/<int:id>/',views.deletebus,name='deletebus'),
    path('update/<int:id>/',views.update_user,name='update'),
    path('updatebus/<int:id>/',views.update_bus,name='update_bus'),
    path('do_update/<int:id>/',views.do_update,name='do_update'),
    path('reservations/', views.user_reservations, name='user_reservations'),
    path('view_reservations/', views.view_reservations, name='view_reservations'),



]
