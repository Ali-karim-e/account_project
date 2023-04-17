from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Account
from django.conf import settings


class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'account/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, '!!you logged in syte!!')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            account = Account.objects.create_user(username=cd['username'], email=cd['email'])
            account.set_password(cd['password1'])
            account.save()
            messages.success(request, 'You register successfully', 'success')
            return redirect('home:home')
        return render(request, self.template_name, {'form': form})

class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, '!!you logged in syte!!')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'You logged in successfully ', 'success')
                return redirect('home:home')
            messages.error(request, 'username or password is wrong', 'warning')
            return render(request, self.template_name, {'form': form})
        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You logged out successfully ', 'success')
        return redirect('home:home')

class UserProfileView(LoginRequiredMixin, View):
    form_class = UserProfileForm
    template_name = 'account/profile.html'

    def get(self, request, user_id, dic={}):
        account = Account.objects.get(pk=user_id)
        form = self.form_class(
            initial={
                'id': account.id,
                'email': account.email,
                'username': account.username,
                'profile_image': account.profile_image
            }
        )
        dic['form'] = form
        dic['user'] = account
        dic['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
        return render(request, 'account/profile.html', dic)

    def post(self, request, user_id, dic={}):
        account = Account.objects.get(pk=user_id)
        form = self.form_class(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Edit profile is successfully', 'success')
            return redirect('home:home')
        else:
            form = self.form_class(request.POST, instance=request.user,
                                   initial={
                                       'id': account.id,
                                       'email': account.email,
                                       'username': account.username,
                                       'profile_image': account.profile_image
                                   }
                                   )
            dic['form'] = form
        return render(request, 'account/profile.html', dic)
