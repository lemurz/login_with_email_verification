from django.contrib.auth.models import User
from . import views
from django.contrib.auth import authenticate, login, logout

def userFirstName(request):
    if request.user.is_authenticated:
        return {'firstName':request.user.first_name}
    else:
        return{'firstName':''}