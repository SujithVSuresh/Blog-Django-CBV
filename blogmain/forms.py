from django import forms
from django.db import models
from django.db.models import fields
from django.forms import ModelForm
from .models import CommentReply, UserProfile, BlogPost, Comment

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['name', 'bio', 'birthday', 'location']

class CreateBlogPostForm(forms.ModelForm):

    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'meta_description', 'author', 'category']  
        widgets = {
            'author': forms.HiddenInput(),
            }    

class PostCommentForm(forms.ModelForm):
    comment_text = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Add Comments'}))

    class Meta:
        model = Comment
        fields = ['comment_text']        

class CommentReplyForm(forms.ModelForm):
    comment_reply_text = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Add Comment Reply'}))

    class Meta:
        model = CommentReply
        fields = ['comment_reply_text']        