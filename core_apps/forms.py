

from django import forms
from .models import Comment, Message, Profile
from django.contrib.auth.models import User


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'content']



class MessageForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(queryset=User.objects.all(), empty_label='Select a recipient')
    #recipient = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'recipient-autocomplete'}))

    class Meta:
        model = Message
        fields = ['recipient', 'content']