from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from login_email import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . tokens import generateToken
from django.template.loader import render_to_string

# Create your views here.
def homepage(request):
    return render(request, 'authentication/index.html')

def signup(request):

    if request.method=='POST' :
        username = request.POST.get('username')
        email = request.POST.get('email')
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')

        if User.objects.filter(username = username):
            messages.error(request, 'This username is already in use')
            return redirect('signup')
        
        if User.objects.filter(email = email).exists():
            messages.error(request, 'This email is already in use')
            return redirect('signup')
        
        if(len(username)>20):
            messages.error(request, 'Username is too long')
            return redirect('signup')
        
        if not username.isalnum():
            messages.error(request, 'Username must only consist of letters and numbers')
            return redirect('signup')
        
        if password != confirmPassword:
            messages.error(request, 'Passwords do not match')
            return redirect('signup') 

        myUser = User.objects.create_user(username, email, password)
        myUser.first_name = firstName
        myUser.last_name = lastName
        myUser.is_active = False
        myUser.save()
        messages.success(request, "Your account has been created successfully. We have sent you a confirmation email")

        #E-mail

        subject = "Welcome to Test Login!"
        message = "Hello " +myUser.first_name+ "!\nPlease follow the link below to confirm your account."
        from_email = settings.EMAIL_HOST_USER
        to_list = [myUser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        #Confirmation E-mail

        currentSite = get_current_site(request)
        confirmSubject = "Confirm your e-mail at Test"

        context = {
            'name' : myUser.first_name,
            'domain' : currentSite.domain,
            'uid' : urlsafe_base64_encode(force_bytes(myUser.pk)),
            'token' : generateToken.make_token(myUser)
        }

        confirmMessage = render_to_string('authentication/confirmation.html', context)

        email = EmailMessage(
            confirmSubject,
            confirmMessage,
            settings.EMAIL_HOST_USER,
            [myUser.email]
        )

        email.fail_silently = True
        email.send()

        return redirect('signin')


    return render(request, 'authentication/signup.html')

def signin(request):

    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return render(request, 'authentication/index.html')
        else:
            messages.error(request, "Wrong Credentials")
            return redirect('')

    return render(request, 'authentication/signin.html')

def signout(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk = uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None
    
    if myuser is not None and generateToken.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect('')
    else:
        return render(request, 'authentication/activatedFailed.html')