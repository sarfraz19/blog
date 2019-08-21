from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User, auth
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import TemplateView, UpdateView
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import Post
from django.contrib.auth import logout as django_logout
from django.core.paginator import Paginator
from django.shortcuts import render
import json
import random

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    View,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
# Create your views here.


def login(request):
    return render(request, 'login.html')


def logout(request):
    django_logout(request)
    return render(request, "logout.html")


def home(request):
    value = random.randint(1000, 9999)
    print(value)
    request.session['value'] = value
    print(request.session['value'])
    if request.method == "POST":
        request.session['name'] = request.POST['name']
        request.session['email'] = request.POST['email']
        request.session['password'] = request.POST['password']
        request.session['date'] = request.POST['date']
        request.session['gender'] = request.POST['gender']
        sub = "Blog OTP"
        msg = "Dear Blogger \n your OTP is " + str(value)
        from_email = settings.EMAIL_HOST_USER
        to = [request.POST['email']]
        print(from_email)
        print(to)
        send_mail(sub, msg, from_email, to)
        print("mail sent")
    return HttpResponse(status=204)


def checkOtp(request):
    print("value")
    value = request.session.get('value')
    print(value)

    name = request.session['name']
    email = request.session['email']
    password = request.session['password']
    request.session['name'] = name
    request.session['email'] = email
    date = request.session['date']
    gender = request.session['gender']
    print(name)

    if request.method == "POST":
        print("otpcheck")
        otpcheck = request.POST['otpval']
        print(otpcheck)
        if otpcheck == str(value):
            print("OTP")
            print("user success")
            user, created = User.objects.get_or_create(
                username=email, first_name=name)
            user.set_password(password)
            user.save()
            print("user created")
        else:
            messages.info(request, 'Invalid OTP')
            return render(response, 'login.html')
    return HttpResponse(status=204)


def checkUser(request):
    if request.method == "POST":
        username = request.POST['emaillog']

        request.session['username'] = username
        print("session")
        print(request.session['username'])
        password = request.POST['passwordlog']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            article_list = Post.objects.all()
            paginator = Paginator(article_list, 2)  # Show 25 contacts per page
            page = request.GET.get('page')
            article = paginator.get_page(page)
            print("query set")
            print(article)
            return render(request, 'post.html', {'article': article, 'article_list':article_list})
        else:
            messages.info(request, 'invalid credentials')
            return redirect('login')
    else:
        article_list = Post.objects.all()
        paginator = Paginator(article_list, 2)  # Show 25 contacts per page
        page = request.GET.get('page')
        article = paginator.get_page(page)
        print("query set")
        print(article)
        return render(request, 'post.html' , {'article': article, 'article_list':article_list})


def newpost(request):
    return render(request, 'newpost.html')


def create(request):
    username = request.session['username']
    print("username")
    print(username)
    user1 = User.objects.get(username=username)
    print(user1.pk)

    if request.method == "POST":
        title = request.POST['title']
        des = request.POST['description']
        po = Post.objects.create(title=title, content=des, author=user1)
        po.save()
        print("post created")
        messages.info(request, 'post created')
        return redirect('postpage')
    else:
        return render(request, 'newpost.html')


def delete(request):
    return render(request, 'deletepost.html ')

def profile(request):
    user = User.objects.get(username = request.session['username'])
    posts = Post.objects.filter(author=user.pk)
    print(user)
    print(user.email)
    print(posts)
    return render(request,'profile.html',{'user':user,'posts':posts})


def postpage(request):
    article_list = Post.objects.all()
    paginator = Paginator(article_list, 2)  # Show 25 contacts per page
    page = request.GET.get('page')
    article = paginator.get_page(page)
    print(article)
    print(article_list)
    return render(request, 'post.html', {'article': article , article_list:'article_list'})

# delete


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "postdelete.html"
    success_url = "/postpage"

    def test_func(self):
        # get current working post
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# update
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = "postupdate.html"
    fields = ["title", "content"]

    

    # method to assign username to author for updating author name in post
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # function to permit editing post based on their ownership
    def test_func(self):
        # get current working post
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDetailView(DetailView):
    model = Post
    template_name = "postdetail.html"
