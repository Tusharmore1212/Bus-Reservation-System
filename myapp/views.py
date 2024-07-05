from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.models import User
import re
from django.contrib.auth.decorators import login_required
from myapp.models import Bus, Reservation
from django.utils import timezone  
from decimal import Decimal
from django.views import View
def home(request):
    return render(request, 'index.html')

class login(View):
    def get(self,request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST['username']
        password = request.POST['password']
        print("working")
        user = authenticate(request, username=email, password=password)
        print(user)

        

        if user is not None:
            request.session['user_id'] = user.id
            request.session['user_name'] = user.email
            auth_login(request, user)
            if user.is_staff:
                print('workin')
                return redirect('/admin_dashboard/')
            else:
                print('workin')
                return redirect('/user_dashboard/')
        else:
            error_message = "Invalid email or password"
            return render(request, 'login.html', {'error_message': error_message})
        

def reg(request):
    if request.method == "POST":
        fname = request.POST['firstName']
        lname = request.POST['lastName']
        email = request.POST['email']
        pswd = request.POST['password']
        cpswd = request.POST['confirmPassword']
        
        if not is_valid_password(pswd):
            error_message = "Enter a valid password"
            return render(request, 'register.html', {'error_message': error_message})
        
        if pswd == cpswd:
            try:
                if User.objects.filter(email=email).exists():
                    error_message = "Email already exists. Please use a different email."
                    return render(request, 'register.html', {'error_message': error_message})
                
                hashed_password = make_password(pswd)
                user = User.objects.create_user(username=email, first_name=fname, last_name=lname, password=pswd,email=email)
                user.save()
                return redirect('/login/')
            except Exception as e:
                error_message = str(e)
                return render(request, 'register.html', {'error_message': error_message})
        else:
            return render(request, 'register.html', {'error_message': 'Passwords do not match'})
    return render(request, 'register.html')

# def log(request):
#     if request.method == "POST":
#         email = request.POST['username']
#         password = request.POST['password']
#         print("working")
#         user = authenticate(request, username=email, password=password)
#         print(user)

        

#         if user is not None:
#             request.session['user_id'] = user.id
#             request.session['user_name'] = user.email
#             auth_login(request, user)
#             if user.is_staff:
#                 print('workin')
#                 return redirect('/admin_dashboard/')
#             else:
#                 print('workin')
#                 return redirect('/user_dashboard/')
#         else:
#             error_message = "Invalid email or password"
#             return render(request, 'login.html', {'error_message': error_message})
#     return render(request, 'login.html')

@login_required(login_url='login')
def user_dashboard(request):
    if not request.user.is_staff:
        return render(request, 'User_dashboard.html')
    else:
        return redirect('/admin_dashboard/')
    
@login_required(login_url='login')
def admin_dashboard(request):
    if request.user.is_staff:
        return render(request, 'admin_dashboard.html')
    else:
        return redirect('/user_dashboard/')
    
@login_required(login_url='login')
def logout_view(request):
    auth_logout(request)
    return redirect('/login/')

def is_valid_password(password):
    if len(password) < 8:
        return False
    if not re.search(r'[a-zA-Z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    return True

@login_required(login_url='login')
def manage_user(request):
    users = User.objects.exclude(username='admin')
    return render(request, 'manage_user.html', {'user': users})

@login_required(login_url='login')
def manage_bus(request):
    buses = Bus.objects.all()
    return render(request, 'manag_bus.html', {'buses': buses})

@login_required(login_url='login')
def update_user(request,id):
    s = User.objects.get(pk=id)
    passn=s.password
    print(passn)
    return render(request, "update_user.html", {"std": s,"passn":passn})

@login_required(login_url='login')
def update_bus(request,id):
    s = Bus.objects.get(pk=id)
    return render(request,"udpate_bus.html", {"buses": s,})

@login_required(login_url='login')
def do_update(request, id):
    if request.method == "POST":
        fname = request.POST['fname']
        email = request.POST['email']
        lname = request.POST['lname']
        passn = request.POST['pass']
        s = User.objects.get(pk=id)
        s.first_name = fname
        s.email = email
        s.last_name = lname
        s.password = passn
        s.save()
        return redirect('/manage_user/')
    
@login_required(login_url='login')
def doupdatebus(request, id):
    if request.method == "POST":
        busname = request.POST['bus_name']
        busno = request.POST['bus_no']
        source = request.POST['source']
        destination = request.POST['destination']
        date = request.POST['date']
        price = request.POST['price']
        s = Bus.objects.get(pk=id)
        s.bus_name = busname
        s.bus_no = busno
        s.source = source
        s.destination = destination
        s.date = date
        s.seat_price = price
        s.save()
        return redirect('/manage_bus/')
    
@login_required(login_url='login')   
def delete(request, id):
    s = User.objects.get(pk=id)
    s.delete()
    return redirect("/manage_user/")

@login_required(login_url='login')
def deletebus(request, id):
    s = Bus.objects.get(pk=id)
    s.delete()
    return redirect("/manage_bus/")

@login_required(login_url='login')
def addbus(request):
    if request.method == "POST":
        busno = request.POST['Bus_no']
        busname = request.POST['Bus_name']
        source = request.POST['source']
        destination = request.POST['destination']
        seat = request.POST['seat']
        date = request.POST['date']
        price = request.POST['price']

        busobj = Bus()
        busobj.bus_no = busno
        busobj.bus_name = busname
        busobj.source = source
        busobj.destination = destination
        busobj.date = date
        busobj.seat = seat
        busobj.seat_price = price

        busobj.save()
        return redirect('/addbus/')
    return render(request, 'add_bus.html')\
    

@login_required(login_url='login')
def search_bus(request):
    buses = None
    username = request.session.get('user_name', '')
    if request.method == 'GET' and 'search' in request.GET:
            source = request.GET['source']
            destination = request.GET['destination']
            date = request.GET['date']
            buses = Bus.objects.all()
            if source:
                buses = buses.filter(source__icontains=source)
            if destination:
                buses = buses.filter(destination__icontains=destination)
            if date:
                buses = buses.filter(date=date)
    return render(request, 'search_bus.html', {'buses': buses,'username':username})
@login_required(login_url='login')
def book_ticket(request):
    if request.method == 'POST':
        try:
            bus_id = int(float(request.POST.get('bus_id')))
            print(bus_id)
            username = request.POST.get('username')
            source = request.POST.get('source')
            destination = request.POST.get('destination')
            date = request.POST.get('date')
            price = request.POST.get('price')
            seat_count = int(request.POST.get('seat'))
            total_amount = Decimal(request.POST.get('amt'))

            user = User.objects.get(username=username)

            bus = Bus.objects.get(id=bus_id)

            reservation = Reservation.objects.create(
                user=user,
                bus=bus,
                num_seats=seat_count,
                total_price=total_amount,
                reservation_date=timezone.now() 
            )

            bus.seat -= seat_count
            bus.save()

            return redirect('/user_dashboard/') 
        except Exception as e:
            error_message = str(e)
            print(error_message)
            return render(request, 'search_bus.html', {'error_message': error_message})

    return redirect('/search_bus/')

@login_required(login_url='login')
def user_reservations(request):
    user = request.user
    reservations = Reservation.objects.filter(user=user)
    return render(request, 'user_reservation.html', {'reservations': reservations})

@login_required(login_url='login')
def view_reservations(request):
    reservations = Reservation.objects.all()
    return render(request, 'view_reservation.html', {'reservations': reservations})

@login_required(login_url='login')
def delete_res(request,id):
    s = Reservation.objects.get(pk=id)
    s.delete()
    return render(request, 'cancel_reservation.html')
@login_required(login_url='login')
def logout_view(request):
    auth_logout(request)
    return redirect('/login/')

