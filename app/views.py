from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
from Deep_Chat.settings import database

# from app import database

# from app import database

# Create your views here.

# python manage.py runserver





def say_hello(self, request):
    template = loader.get_template('hello.html')
    return HttpResponse(template.render())

def welcome(request):    
    return render(request, "welcome.html")

def login(request):
    
    user = request.POST.get('user')
    passw = request.POST.get("password")
    
    if user is not None and passw is not None:
        database.Authenticate(user, passw)

        if database.is_authenticated:
            context = database.ViewFeed()
            
            return render(request, "townsquare.html", context)
        
        else:
            return render(request, 'welcome.html'
            , {'message': 'Invalid credentials'}
            )
    else: 
        return render(request, 'login.html')

def signup(request):
    user = request.POST.get('user')
    passw = request.POST.get("password")

    if user is not None and passw is not None:
        database.Authenticate(user, passw)
        if database.MakeUser(user, passw):
            return render(request, "welcome.html", {'message': 'Sign-up successful, now you can log in'})
        else:
            return render(request, 'welcome.html', {'message': 'User already exists'})
    else:
        return render(request, "signup.html")

def makepost(request):
    post = request.POST.get('post')

    if post is not None:
        database.MakePost(post)
        context = database.ViewFeed()
            
        return render(request, "townsquare.html", context)
        

    else:
       return render(request, 'makepost.html')








