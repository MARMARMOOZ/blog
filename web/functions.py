#importing needed models
from .models import Topic, Comments, Token
from random import randint
from hashlib import sha1,sha256
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
#function that makes new topics
def new_topic(title, content, date,token):
    #publisher user
    user = User.objects.get(token=Token.objects.get(token=token))
    #base content of html files in topics
    file_content = """{% extends "topic_base.html" %}
{% load static %}
{% block title %}"""+title+"""{% endblock %}
{% block subject %}"""+title+"""{% endblock %}
{% block date %}"""+str(date)+"""{% endblock %}
{% block content %}
"""+content+"""
{% endblock %}
{% block comments %}
{{ msg }}
{% endblock %}"""
    #openning new html file for topic
    #TODO:
    # 1: make html filename based on topic number and linked on urls.py with topic name(the " " charachter and other non-agreed charachter get replaced)
    # 2: file address get found by os methods not manual
    file = open(f"C:\\Users\\USER\\Desktop\\Django\\blog\\templates\\{title}.html",'a')
    file.write(file_content)
    file.close()
    #making new filed in Topic model for our topic
    #TODO:
    # 1: make a system that a person cant make too many topics in a specefic time
    # 2: make a system that cant make two topics with same main information(title,textn_tags,id,topic_number and etc.)
    Topic(title=title,datepublished=date,textn_tags=content,user=user).save()
    #storing last(our) topic number into a variable
    topic_number = Topic.objects.all().last().id
    #storing python django code that makes a view for our topic included comment writing option
    view_code = f"""def topic{topic_number}(request):
    topic_id = {topic_number}
    if request.method == "POST":
        comment = request.POST['comment']
        token = request.POST['token']
        write_comment(topic_id,token,comment)
        return render(request,"{title}.html",{'msg':'sucssesfull.'})
    return render(request,\"{title}.html\")
"""
    #open app views.py file
    file = open("C:\\Users\\USER\\Desktop\\Django\\blog\\web\\views.py",'a')
    #write view code and close file
    file.write(view_code)
    file.close()
    #open urls.py file 
    file = open('C:\\Users\\USER\\Desktop\\Django\\blog\\blog\\urls.py', 'a')
    #store code that link our views.py view to urls.py urlpatterns
    urls_code = f"""
urlpatterns.append(path('{title}/', views.topic{topic_number}))"""
    #writing that
    file.write(urls_code)
#function to writing comments
def write_comment(topic_id, user_token, comment):
    #storing user token
    token = Token.objects.get(token=user_token)
    #creating our user comment field
    Comments.objects.create(topic_id=topic_id,user_token=token,comment=comment)
    #finding name of the topic filename with views.py view topic_id
    topic_filename = Topic.objects.filter(id=topic_id).first().title + '.html'
    #finding user username based of user token
    username = Token.objects.filter(token=user_token).first().user.username
    #html code for our user comment code
    comment_code = """
<h3>"""+username+""" said:</h3>
<h4>"""+comment+"""</h4>
{% endblock %}
"""
    #opening file based of topic_filename
    file = open(f"C:\\Users\\USER\\Desktop\\Django\\blog\\templates\\{topic_filename}", 'r')
    #reading all our file line codes and storing in list
    lines = file.readlines()
    #writing comment code in last line of file
    lines[len(lines)-1] = comment_code
    file = open(f"C:\\Users\\USER\\Desktop\\Django\\blog\\templates\\{topic_filename}", 'w')
    #writing code into it
    file.writelines(lines)
    file.close()
#Token generator function
def Generate_Token():
    charachters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    raw_token = ""
    for i in range(16):
        raw_token += charachters[randint(0,len(charachters)-1)]
    token = sha1(raw_token.encode()).hexdigest()
    return token
#generate and return a valid token
def Token_Generator():
    user_token = ""
    token_not_created = True
    while(token_not_created):
        tmp_user_token = Generate_Token()
        try:
            token_query = Token.objects.get(token=tmp_user_token)
        except:
            user_token = tmp_user_token
            token_not_created = False
    return user_token
#function to register
def register(username,email,password):
    user = User.objects.create_user(username=username,email=email,password=password)
    token = Token.objects.create(user=user, token=Token_Generator())
    return token.token
#function to login
def login(username, email, password):
    user = authenticate(username=username,email=email,password=password)
    token = Token.objects.get(user=user).token
    return token