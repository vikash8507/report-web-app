from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

def logout_view(request):
    logout(request)
    return redirect('login')


def login_view(request):

    if request.user.is_authenticated:
        return redirect('sales:home')

    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('sales:home')
    
    context = {
        'form': form,
    }

    return render(request, 'login.html', context)