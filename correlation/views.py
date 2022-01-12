import json
from datetime import datetime, timedelta

from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import (HttpResponse, HttpResponseNotFound,
                         HttpResponseRedirect, JsonResponse)
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from scipy.stats.stats import pearsonr   

from .models import User, Data_type, Correlation_data

def index(request):

    if(Data_type.objects.all().count() == 0):
        Data_type.objects.create(type_name='steps')
        Data_type.objects.create(type_name='pulse')

    print(Data_type.objects.all(), 'ALL')
    print(Correlation_data.objects.all(), 'Data')

    if request.user.is_authenticated:
        return render(request, "correlation/index.html")
    else:
        return render(request, "correlation/login.html")

def check_dates(arr, date):
    flag = True
    print(arr, 'arr')
    for a in arr:
      print(a['date'], 'a')
      if a['date'] == date:
          continue
      else:
          flag = False
          break
    return flag

def create_type(request, name):
    Data_type.objects.create(type_name=name)
    return render(request, "correlation/index.html")

def extract_numbers(arr):
    new_arr = []
    flag = True
    print(arr, 'arr')
    for a in arr:
      if 'value' in a and type(float( a['value'] )) == float:
        print(type(float( a['value'] )) == float, 'a')
        new_arr.append(float( a['value'] ))
      else:
        flag = False
        break
        
    if flag:
      return new_arr
    else:
      return False 

def verification_received_data(row_data):
    x_arr = extract_numbers(row_data['data']['x'])
    y_arr = extract_numbers(row_data['data']['y'])
    print(x_arr, 'xarr')
    print(y_arr, 'yarr')
    date = row_data['data']['x'][0]['date']
    x_dates = []
    y_dates = []
    if(x_arr and y_arr):
      x_dates = check_dates(row_data['data']['x'], date)
      y_dates = check_dates(row_data['data']['y'], date)
      print(x_dates, 'x_dates')
      print(y_dates, 'y_dates')
      if len(x_arr) != len(y_arr) :
        return False
      else:
        return (x_arr, y_arr) 
    else:
      return False
    
def correlation_view(request):
    print(request.GET, 'request')
    data = request.GET.copy()
    x_data_str = data["x_data_type"]
    y_data_str = data["y_data_type"]
    user_id = data["user_id"]
    print(x_data_str, y_data_str, user_id, 'LDJLKJLJ')
    try:
        curr_user = User.objects.get(id=user_id)
        try:
            x_data_type = Data_type.objects.get(type_name=x_data_str)
            try:
                y_data_type = Data_type.objects.get(type_name=y_data_str)
                try:
                    answ = Correlation_data.objects.filter(user=curr_user, 
                            x_data=x_data_type,
                            y_data=y_data_type,
                            )               
                    print([a.serialize() for a in  answ ], "answ")
                    return JsonResponse( {"answer": [a.serialize() for a in  answ ]})
                except Correlation_data.DoesNotExist:
                    return HttpResponseNotFound()
            except Data_type.DoesNotExist:
                return HttpResponseNotFound()
        except Data_type.DoesNotExist:
            print(Data_type.objects.get(type_name='steps'), 'ALL')
            return HttpResponseNotFound()
    except User.DoesNotExist:
        return HttpResponseNotFound()

def calc_p(ver_data):
    if(ver_data):
          (a, b) = ver_data   
          result = pearsonr(a,b)
          print(result, 'result')
          return result
    else:
          return False 

def calculate_view(request):
    message = ''
    if request.method == "POST":
        row_data = json.loads(request.body)
        print(row_data, 'LJLJLKJ')
        try:
            curr_user = User.objects.get(id=row_data["user_id"])
            try:
                x_data_type = Data_type.objects.get(type_name=row_data['data']['x_data_type'])
                try:
                    date_c = row_data['data']['x'][0]['date']
                    print(date_c, "DATE")
                    x_data_type = Data_type.objects.get(type_name=row_data['data']['x_data_type'])
                    y_data_type = Data_type.objects.get(type_name=row_data['data']['y_data_type'])
                    c = calc_p(verification_received_data(row_data))

                    new_correlation = Correlation_data.objects.create(user=curr_user, 
                            x_data=x_data_type,
                            y_data=y_data_type,
                            correlation=c[0],
                            correlation_p=c[1],
                            day_name=date_c
                            )
                    message = 'new correlation is created'
                except Data_type.DoesNotExist:
                    message = "There is no such type in the system"
            except Data_type.DoesNotExist:
                message = "There is no such type in the system"
 
        except User.DoesNotExist:
            message = "There is no such user in the system"
        print(message, MESSAGE)
        return message
    else:
        print(message, MESSAGE)
        return HttpResponseNotFound()


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "correlation/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "correlation/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "correlation/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "correlation/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"), {"status": "OK"})
    else:
        return render(request, "correlation/register.html")

