from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django import views
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from twitter import models
from twitter import forms

# Create your views here.
from twitter.forms import TweetForm, MessageModelForm
from twitter.models import Tweet, Message


class LoginNewView(View):
    def get(self, request):
        form = AuthenticationForm()
        ctx = {'form': form}
        return render(request, 'twitter/user.html', ctx)

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('twitter/twitter:index')
        ctx = {'form': form}
        return render(request, 'twitter/user.html', ctx)


class AddUserView(View):
    def get(self, request):
        form = UserCreationForm()
        ctx = {'form': form}
        return render(request, 'twitter/signup.html', ctx)

    def post(self, request):
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['username']
            form.save()
            user = User.objects.get(username=user_name)
            login(request, user)
            return redirect('twitter/twitter:index')
        ctx = {'form': form}
        return render(request, 'twitter/signup.html', ctx)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('twitter/twitter:login')


class MainWebpageView(views.View):
    def get(self, request):
        tweets = models.Tweet.objects.order_by('-creation_date')
        ctx = {'tweets': tweets}
        return render(request, 'twitter/index.html', ctx)


class TweetComposeView(LoginRequiredMixin, View):
    def get(self, request, id):
        user = id
        # template_name = "tweet_form.html" nie potrzebujemy template_name ponieważ mamy template odpowiednio nazwany i Django sam go wyszuka.
        form = TweetForm()  # normalnie nie wymaga formularza ale tu zmienaimy wiget na textarea, żeby mieć większe okienko do wpisywania treści tweet
        user_id = User.objects.get(id=user)
        posts = Tweet.objects.filter(author=user_id)
        ctx = {'form': form,
               'posts': posts}
        return render(request, 'twitter/tweet_form.html', ctx)

    def post(self, request, id):
        form = TweetForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user  # wyciagamy autora z requesta, nie może go sam wpisywać bo mógłby się podszyć pod kogoś.
            form.save()
            return redirect('twitter/twitter:index')


class MessageView(LoginRequiredMixin, View):
    def get(self, request, id):
        form = MessageModelForm()
        messages = Message.objects.filter(to_user=id)
        ctx = {'form': form,
               'messages': messages}
        return render(request, "twitter/message.html", ctx)

    def post(self, request, id):
        form = MessageModelForm(request.POST)
        if form.is_valid():
            to_user_from_form = form.cleaned_data['to_user']
            subject_from_form = form.cleaned_data['subject']
            content_from_form = form.cleaned_data['content']
            user_from_form = request.user
            new_user = Tweet.objects.filter(author=user_from_form)
            for user_to_save in new_user:
                user_to_save = new_user[0]
                from_user_from_form = new_user[0].author
                print('kupa')
                if from_user_from_form != to_user_from_form:
                    print(user_to_save, to_user_from_form)
                    new_message = Message(to_user=to_user_from_form,
                                          from_user=user_to_save,
                                          subject=subject_from_form,
                                          content=content_from_form)
                    new_message.save()
                    return redirect('twitter/twitter:index')
                return redirect('twitter/twitter:message', id)


class OpenMessageView(LoginRequiredMixin, View):
    def get(self, request, message_id):
        message = Message.objects.get(id=message_id)
        ctx = {'subject': message.subject,
               'content': message.content}
        return render(request, "twitter/openmessage.html", ctx)
