import json
from datetime import datetime, timedelta

from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import (Http404, HttpResponse, HttpResponseNotFound,
                         HttpResponseRedirect, JsonResponse)
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView
from scipy.stats.stats import pearsonr

from .models import Correlation_data, Data_type, User


class TypesListView(ListView):
    model = Data_type 

    class Meta:
        model = Data_type 
        fields = ["type_name"]


    def get_types(self):
        list_t = Data_type.objects.all()
        return list_t



def index(request):

    list_t = TypesListView().get_types()

    if request.user.is_authenticated:
        return render(request, "correlation/index.html", { 'types': [a for a in list_t] })
    else:
        return render(request, "correlation/login.html")

def check_dates(arr, date):
    flag = True
    for a in arr:
      if a['date'] == date:
          continue
      else:
          flag = False
          break
    return flag

def create_type(request):
    if request.method == "POST":
        try:
            Data_type.objects.get(type_name=request.POST['type_name'])
        except Data_type.DoesNotExist:
            new_type = Data_type.objects.create(type_name=request.POST['type_name'])
    return HttpResponseRedirect(reverse("index"))


def delete_type(request, type_id):
    try:
        Data_type.objects.get(id=type_id).delete()
        return HttpResponseRedirect(reverse("index"))
    except Data_type.DoesNotExist:
        return HttpResponseNotFound()

def extract_numbers(arr):
    new_arr = []
    flag = True
    for a in arr:
      if 'value' in a and type(float( a['value'] )) == float:
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
    date = row_data['data']['x'][0]['date']
    x_dates = []
    y_dates = []
    if(x_arr and y_arr):
      x_dates = check_dates(row_data['data']['x'], date)
      y_dates = check_dates(row_data['data']['y'], date)
      if len(x_arr) != len(y_arr) :
        return False
      else:
        return (x_arr, y_arr) 
    else:
      return False
    
def correlation_view(request):
    data = request.GET.copy()
    x_data_str = data["x_data_type"]
    y_data_str = data["y_data_type"]
    user_id = data["user_id"]
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
                    return JsonResponse( {"answer": [a.serialize() for a in  answ ]})
                except Correlation_data.DoesNotExist:
                    raise Http404
            except Data_type.DoesNotExist:
                raise Http404
        except Data_type.DoesNotExist:
            raise Http404
    except User.DoesNotExist:
        raise Http404

def calc_p(ver_data):
    if(ver_data):
          (a, b) = ver_data   
          result = pearsonr(a,b)
          return result
    else:
          return False 

def calculate_view(request):
    if request.method == "POST":
        row_data = json.loads(request.body)
        try:
            curr_user = User.objects.get(id=row_data["user_id"])
            try:
                x_data_type = Data_type.objects.get(type_name=row_data['data']['x_data_type'])
                try:
                    date_c = row_data['data']['x'][0]['date']
                    x_data_type = Data_type.objects.get(type_name=row_data['data']['x_data_type'])
                    y_data_type = Data_type.objects.get(type_name=row_data['data']['y_data_type'])
                    c = calc_p(verification_received_data(row_data))
                    try:
                        for_update = Correlation_data.objects.get(user=curr_user,
                            x_data=x_data_type,
                            y_data=y_data_type,
                            day_name=date_c
                            )
                        for_update.correlation = c[0]
                        for_update.correlation_p = c[1]
                        for_update.save()
                        return HttpResponseRedirect(reverse("index"), status=200)

                    except Correlation_data.DoesNotExist:
                        new_correlation = Correlation_data.objects.create(user=curr_user, 
                            x_data=x_data_type,
                            y_data=y_data_type,
                            correlation=c[0],
                            correlation_p=c[1],
                            day_name=date_c
                            )
                        return HttpResponseRedirect(reverse("index"), status=200)
                except Data_type.DoesNotExist:
                    raise Http404
            except Data_type.DoesNotExist:
                raise Http404
        except User.DoesNotExist:
            raise Http404
    else:
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

