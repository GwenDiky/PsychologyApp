from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib import messages

from accounts.forms import RegisterUserForm


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            user.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Вы вошли в аккаунт.")
            return redirect('main:home')

    else:
        form = RegisterUserForm()
    return render(request, 'registration/register_user.html', {'form': form, })
