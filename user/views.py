# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
  
  
#################### index#######################################
def index(request):
    return render(request, 'index.html', {'title':'index'})
  
########### register here #####################################
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            ######################### mail system ####################################
            htmly = get_template('Email.html')
            d = { 'username': username }
            subject = 'welcome'
            from_email = 'sg247938@gmail.com'
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, email)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            ##################################################################
            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form, 'title':'reqister here'})
  
################ login forms###################################################
def Login(request):
    if request.method == 'POST':
  
        # AuthenticationForm_can_also_be_used__
  
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, f' wecome {username} !!')
            return redirect('/')
        else:
            messages.info(request, f'account done not exit , plz sign up')
            return redirect('/register')
    form = AuthenticationForm()
    return render(request, 'login.html', {'form':form, 'title':'log in'})


def logoutuser(request):
    logout(request)
    return redirect("/login")
