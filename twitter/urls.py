
from django.urls import path
from twitter import views #nie musimy importować konkretnych nazw, bo przez nazwą widoku jest views.

app_name = 'twitter'
urlpatterns = [
    path('', views.MainWebpageView.as_view(), name = 'index'),
    path('compose', views.TweetComposeView.as_view(), name = 'compose')
]
