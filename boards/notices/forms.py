from django import forms
from .models import Board, Notice

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['name', 'is_private']
        labels = {
            'name': 'Board name:',
            'is_private': 'Set as private?'
        }

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content']
        labels = {
            'title': 'Set a title:',
            'content': 'Notice contents:'
        }