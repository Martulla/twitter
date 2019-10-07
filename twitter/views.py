from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django import views
from django.urls import reverse_lazy
from django.views.generic import CreateView

from twitter import models
from twitter import forms

# Create your views here.
from twitter.models import Tweet


class MainWebpageView(views.View):
    def get(self, request):
        tweets = models.Tweet.objects.order_by('-creation_date')
        ctx = {'tweets': tweets}
        return render(request, 'twitter/index.html', ctx)

class TweetComposeView(LoginRequiredMixin, CreateView):
        model = models.Tweet
        #template_name = "tweet_form.html" nie potrzebujemy template_name ponieważ mamy template odpowiednio nazwany i Django sam go wyszuka.
        form_class = forms.TweetForm #normalnie nie wymaga formularza ale tu zmienaimy wiget na textarea, żeby mieć większe okienko do wpisywania treści tweeta
        success_url = reverse_lazy('twitter:compose')

        def form_valid(self, form):
            form.instance.author = self.request.user #wyciagamy autora z requesta, nie może go sam wpisywać bo mógłby się podszyć pod kogoś.
            return super().form_valid(form)
