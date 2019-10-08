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
from twitter.models import Tweet


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


class TweetComposeView(LoginRequiredMixin, CreateView):
    model = models.Tweet
    # template_name = "tweet_form.html" nie potrzebujemy template_name ponieważ mamy template odpowiednio nazwany i Django sam go wyszuka.
    form_class = forms.TweetForm  # normalnie nie wymaga formularza ale tu zmienaimy wiget na textarea, żeby mieć większe okienko do wpisywania treści tweeta
    success_url = reverse_lazy('twitter/twitter:index')

    def form_valid(self, form):
        form.instance.author = self.request.user  # wyciagamy autora z requesta, nie może go sam wpisywać bo mógłby się podszyć pod kogoś.
        return super().form_valid(form)

