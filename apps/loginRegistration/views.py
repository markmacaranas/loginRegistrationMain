from django.shortcuts import render, redirect, HttpResponse
from .models import User
from django.contrib import messages
# Create your views here.

def index(request):
    return render(request, "loginRegistration/index.html")


def process(request):
    # 0 is True or False; 1 is Users or errors
    if request.method != 'POST':
        return redirect ('/')
    else:
        user_valid = User.objects.validate(request.POST)
        if user_valid[0]:
            print "Got user valid true"
            request.session["id"] = user_valid[1].id #user_valid[1] will always be Users
            return redirect ('/success')
        else:
            for message in user_valid[1]:
                messages.add_message(request, messages.INFO, message) #built-in flash functions in Django, add message is default
            return redirect ('/')

def success(request):
    if "id" not in  request.session:
        return redirect ('/')
    try:
        user = User.objects.get(id=request.session["id"])
        context = {
            "user" : user
        }
    except User.DoesNotExist:
        message.add_message(request, messages.INFO, message)
        return redirect ('/')
    messages.info(request,"You have successfully registered {}!".format(user.first_name))
    return render(request, 'loginRegistration/success.html', context)
    return redirect('/process')

def login(request):
    if request.method != 'POST':
        return redirect('/')
    else:
        user = User.objects.authenticate(request.POST)
        if user[0] == True:
            request.session['id'] = user[1].id
            messages.info(request,"You have successfully login {}!".format(user[1].first_name))
            return redirect ('/success')
        else:
            messages.add_message(request, messages.INFO, user[1])
            return redirect ('/')

def logout(request):
    if "id" in request.session:
        request.session.pop("id")
    return redirect ('/')
