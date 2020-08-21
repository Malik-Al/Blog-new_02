from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.generic import DetailView, UpdateView

from accounts.forms import UserCreationForm, UserChangeForm, UserChangePasswordForm
from django.contrib.auth.models import User
from accounts.models import Token, Profile
from main.settings import HOST_NAME



def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user_1 = User(
                email=form.cleaned_data['email'],
                is_active=False)
            user = form.save()
            token = Token.objects.create(user=user)
            activation_url = HOST_NAME + reverse('accounts:user_activate') + '?token={}'.format(token)

            user_1.email_user('Регистрация на сайте localhost',
                              'Для активаций перейдите по ссылке:{}'.format(activation_url))
            login(request, user)
            user.save()
            Profile.objects.create(user=user)
            return redirect('webapp:index')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', context={'form': form})



def user_activate(request):
    token_value = request.GET.get('token')
    try:
        token = Token.objects.get(token=token_value)
        user = token.user
        user.is_active = True
        user.save()
        token.delete()
        login(request, user)
        return redirect('webapp:index')
    except Token.DoesNotExist:
        return redirect('webapp:index')



class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'





class UserChangeView(UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'user_update.html'
    form_class = UserChangeForm
    context_object_name = 'user_obj'

    def test_func(self):
        return self.get_object() == self.request.user

    def get_success_url(self):
        return reverse('accounts:user_detail', kwargs={'pk': self.object.pk})




class UserChangePasswordView(UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'user_password_change.html'
    form_class = UserChangePasswordForm
    context_object_name = 'user_obj'

    def test_func(self):
        return self.get_object() == self.request.user

    def get_success_url(self):
        return reverse('accounts:user_detail', kwargs={'pk': self.object.pk})



























