from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import BlogPost, ContactMessage, GalleryImage, Project, Skill


class ThemedAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
    )


class BaseStyledForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')


class SkillForm(BaseStyledForm):
    class Meta:
        model = Skill
        fields = ['name', 'level', 'proficiency', 'icon']
        widgets = {
            'proficiency': forms.NumberInput(attrs={'min': 0, 'max': 100}),
        }


class ProjectForm(BaseStyledForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'category', 'demo_url', 'source_url', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class GalleryForm(BaseStyledForm):
    class Meta:
        model = GalleryImage
        fields = ['title', 'image']


class BlogForm(BaseStyledForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image', 'is_published']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6}),
        }


class ContactForm(BaseStyledForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }

