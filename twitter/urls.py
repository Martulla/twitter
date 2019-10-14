
from django.urls import path
from twitter import views #nie musimy importować konkretnych nazw, bo przez nazwą widoku jest views.

app_name = 'twitter/twitter'
urlpatterns = [
    path('', views.MainWebpageView.as_view(), name='index'),
    path('compose/<int:id>', views.TweetComposeView.as_view(), name='compose'),
    path('login', views.LoginNewView.as_view(), name='login'),
    path('registration', views.AddUserView.as_view(), name='registration'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('message/<int:id>', views.MessageView.as_view(), name='message'),
    path('openmessage/<int:message_id>', views.OpenMessageView.as_view(), name='openmessage'),
    path('receivedmessage/<int:user_id>', views.ReceivedMessageView.as_view(), name='receivedmessage'),
    path('sendmessage/<int:user_id>', views.SendMessageView.as_view(), name='sendmessage'),
]
