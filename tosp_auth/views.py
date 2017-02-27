from django.shortcuts import redirect, render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate


def logout(request):
    auth_logout(request)
    return redirect('/')


def login(request):
    """ This view deals with login requests.

    In the case of a POST request, the view authenticates the user and
    logs him in. If it receives any other type of request, the view
    renders the login form.

    Parameters
    ----------
    POST['username'] : string
        username of the user that will be authenticated
    POST['password'] : string
        password of the user that will be authenticated
    """
    error_message = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth_login(request, user)
            return redirect('home')
        else:
            error_message = 'El usuario o la contraseña son incorrectos.'
    context = {'error_message': error_message}
    return render(request, 'tosp_auth/login.html', context)
