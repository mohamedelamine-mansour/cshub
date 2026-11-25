from django import forms
from .models import Comment, Post, Report

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('community', 'title', 'body')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {'body': forms.Textarea(attrs={'rows': 3, 'dir': 'auto'})}
        labels = {'body': 'Your comment'}


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('reason',)
        widgets = {'reason': forms.Textarea(attrs={'rows': 4, 'dir': 'auto'})}
        labels = {'reason': 'Why are you reporting this post?'}        