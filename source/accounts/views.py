from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from accounts.forms import UserCreationForm
from django.contrib.auth.models import User

from accounts.models import Token


def login_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('webapp:index')
        else:
            context['has_error'] = True
    return render(request, 'login.html', context=context)





def logout_view(request):
    logout(request)
    return redirect('webapp:index')



def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user_1 = User(
                email=form.cleaned_data['email'],
                is_active=False)
            user = form.save()
            token = Token.objects.create(user=user)
            activation_url = reverse('accounts:user_activate') + '?token={}'.format(token)

            user_1.email_user('Регистрация на сайте localhost',
                              'Для активаций перейдите по ссылке:{}'.format(activation_url))
            login(request, user)
            return redirect('webapp:index')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', context={'form': form})






























