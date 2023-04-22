from django import forms
from django.core.exceptions import ValidationError
from .models import Account


class UserRegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        user = Account.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This email already exists!!')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        user = Account.objects.filter(username=username).exists()
        if user:
            raise ValidationError(' This user already exists!!')
        return username

    def clean(self):
        cd = super().clean()
        password1 = cd.get('password1')
        password2 = cd.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('password must match')

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserProfileForm(forms.ModelForm):
    profile_image = forms.ImageField(widget=forms.FileInput)

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'profile_image', 'bio')

    def save(self, commit=True):
        account = super(UserProfileForm, self).save(commit=False)
        account.first_name = self.cleaned_data['first_name']
        account.last_name = self.cleaned_data['last_name']
        account.profile_image = self.cleaned_data['profile_image']
        if commit:
            account.save()
        return account
