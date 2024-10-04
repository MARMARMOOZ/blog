from django.shortcuts import render, HttpResponse
from .models import Topic
from .functions import new_topic, write_comment, register, login
from datetime import date
# Create your views here.

#TODO:
# 1: when user submit post request after being submit, the post request in browser history get deleted
#new topic page
def new_topic_page(request):
    #if user submit post
    if request.method == "POST":
        if request.COOKIES.get('token') is None:
            return HttpResponse('register or login first.')
        title = request.POST['title']
        textn_tags = request.POST['textn_tags']
        datee = date.today()
        token = request.cookies['token']
        new_topic(title,textn_tags,datee,token)
        return render(request,'new_topic_form.html', {'msg':'Was Sucessfull!'})
    else:
        return render(request,'new_topic_form.html',)
#register page
def register_page(request):
    if request.method == "POST" and request.COOKIES.get('token') is None:
        username = request.POST['username']
        if username is None:
            username = ''
        password = request.POST['password']
        if password is None:
            password = ''
        email = request.POST['email']
        if email is None:
            email = ''
        register(username,email,password)
        return render(request,"register.html",{'msg':'succsesfull!'})
    elif request.COOKIES.get('token') is None:
        return render(request,"register.html")
    elif request.COOKIES.get('token') is not None: return HttpResponse('You are Already in Your Account<br/>Do You want to <a href="/logout/"><strong>logout</strong></a>?')
    else:
        return HttpResponse('Invalid Error')
#login page:
def login_page(request):
    if request.method == "POST" and request.COOKIES.get('token') is None:
        username = request.POST['username']
        if username is None:
            username = ''
        password = request.POST['password']
        if password is None:
            password = ''
        email = request.POST['email']
        if email is None:
            email = ''
        token = login(username,email,password)
        response = render(request,'login.html',{'msg':'welcome.'})
        response.cookies['token'] = token
        return response
    elif request.COOKIES.get('token') is None:
        return render(request, 'login.html')
    elif request.COOKIES.get('token') is not None: return HttpResponse('You are Already in Your Account<br/>Do You want to <a href="/logout/"><strong>logout</strong></a>?')
    else:
        return HttpResponse('Invalid Error')
#topcis segment:
def topic1(request):
    topic_id = 1
    if request.method == "POST":
        #TODO:
        # first authenticate user exist or not 
        if request.COOKIES.get('token') is None:
            return HttpResponse('register or login first.')
        else:
            comment = request.POST['comment']
            token = request.cookies['token']
            write_comment(topic_id,token,comment)
            return render(request,"web.html",{'msg':'sucssesfull.'})
    return render(request,"web.html")
