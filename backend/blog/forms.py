
from blog.models import Category,Post
from typing import Required
from django import forms
from django.contrib.auth.models import User
from django.contrib .auth import authenticate
from django import forms
from .models import Post, Category


class contactform(forms.Form):
    name= forms.CharField(label='name',max_length=100,required=True)
    email= forms.EmailField(label='email',required=True)
    message=forms.CharField(label='message',required=True)

class Registerform(forms.ModelForm):
    username = forms.CharField(label="username",max_length=100,required=True)
    email = forms.EmailField(label="email",max_length=1000,required=True)
    password = forms.CharField(label="password",required=True,max_length=10000)
    password_confirm = forms.CharField(label="password_confrim",max_length=100,required=True)

    class Meta:
        model = User
        fields = ['username' ,'email','password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password!=password_confirm:
            raise forms.ValidationError("password do not match")    

class Loginform(forms.Form):
     username = forms.CharField(label="username",max_length=100,required=True)
     password = forms.CharField(label="password",required=True,max_length=10000)
     def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username,password=password)
        if user is None:
            raise forms.ValidationError("invalid username or password!")
    
class Forgotpasswordform(forms.Form):
    email=forms.EmailField(label='email',max_length=256,required=True)
    username = forms.CharField(label='username',max_length=100,required=True)
    def clean(self):
        cleaned_data=super().clean()
        email=cleaned_data.get('email')
        username =cleaned_data.get('username')
        if not User.objects.filter(email=email,username=username).exists():
            raise forms.ValidationError("given email id is not exists")

class resetpasswordform(forms.Form):
    new_password = forms.CharField(label='new_password',min_length=8)
    confirm_password = forms.CharField(label='new_password',min_length=8)
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password!=confirm_password:
            raise forms.ValidationError("password do not match")  
      
class PostForm(forms.ModelForm):
    title = forms.CharField(
        label='Title',
        max_length=100,
        required=True
    )
    content = forms.CharField(
        label='Content',
        widget=forms.Textarea,
        required=True
    )
    category = forms.ModelChoiceField(
        label='Category',
        queryset=Category.objects.all(),
        required=True
    )
    img_url = forms.ImageField(
        label='Image',
        required=False
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'img_url']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if title and len(title) < 5:
            self.add_error('title', 'Title must contain at least 5 characters.')

        if content and len(content) < 10:
            self.add_error('content', 'Content must contain at least 10 characters.')

        return cleaned_data

    def save(self, commit=True):
        post = super().save(commit=False)

        # If image not uploaded, set default image URL
        if not self.cleaned_data.get('img_url'):
            post.img_url = (
                "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"
            )

        if commit:
            post.save()

        return post

