from django import forms

from twitter import models
from twitter.models import Message


class LoginForm(forms.Form):
    login = forms.CharField(max_length=120)
    password = forms.CharField(widget=forms.PasswordInput)


class TweetForm(forms.ModelForm):
    class Meta:
        model = models.Tweet
        fields = ['content']
        widgets = {'content': forms.Textarea()}


class MessageModelForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ['date_sent', 'from_user', 'status']


