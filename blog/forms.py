from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
# from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from blog.models import Post, Profile

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    fname = forms.CharField(required=True, max_length=15)
    lname = forms.CharField(required=True, max_length=15)

    class Meta:
        model = User
        fields = ("username", "fname", "lname", "email", "password1", "password2")
    
    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class User_Post(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category','post_image',]
        prepopulated_fields = {'slug': ('title', 'created_by','category','id', 'created_at',)}


class User_Profile(ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date', 'website','facebook','linkedin','instagram','youtube','profile_image',]