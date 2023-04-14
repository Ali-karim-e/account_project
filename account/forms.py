from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Account


class UserRegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This email already exists!!')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError(' This user already exists!!')
        return username

    def clean(self):
        cd = super().clean()
        p1 = cd.get('password1')
        p2 = cd.get('password2')
        if p1 and p2 and p1 != p2:
            raise ValidationError('password must match')

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserProfileForm(forms.ModelForm):
    profile_image = forms.ImageField(widget=forms.FileInput)

    class Meta:
        model = Account
        fields = ('username', 'email', 'profile_image', 'bio')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        account = Account.objects.filter(email=email).exists()
        if account:
            raise ValidationError('This email already exists!!')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        account = Account.objects.filter(username=username).exists()
        if account:
            raise ValidationError('This username already exists!!')
        return username
    def save(self, commit=True):
        account = super(UserProfileForm, self).save(commit=False)
        account.username = self.cleaned_data['username']
        account.email = self.cleaned_data['email'].lower()
        account.profile_image = self.cleaned_data['profile_image']
        if commit:
            account.save()
        return account
