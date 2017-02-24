from django.shortcuts import redirect, render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .forms import LoginForm


def logout(request):
    auth_logout(request)
    return redirect('/')

def login(request):
    if request.method == 'POST':
        #form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        #username = form.get('username')
        #password = form.get('password')
        #print(username)
        #print(password)
        #user = authenticate(username=username, password=password)
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                #return render(request,'base/home.html')
                return redirect('/')
                #redirect to the success page
            else:
                #form = LoginForm()

                return render(request,'tosp_auth/login.html')
                #return render(request,'login/login.html', {'form': form})
        else:
            #form = LoginForm()
            #print('Login invalido {} {} '.format(username,password))
            return render(request,'tosp_auth/login.html')
            #return render(request,'login/login.html', {'form': form})
            # Return an 'invalid login' error message.
    else:
        #form = LoginForm()
        return render(request,'tosp_auth/login.html')
        #return render(request, 'login/login.html', {'form': form})
