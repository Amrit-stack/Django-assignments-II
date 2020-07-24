from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import LoginForm, SignUpForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
USER = get_user_model()


def login_view(request):
    if request.method == 'POST':
        print(request.POST)
        form = LoginForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                print("A user is found", user)
                login(request, user)
                return redirect('/user/profile/')
            else:
                print('Auth credentials do not match')
    elif request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/user/profile/')
        form = LoginForm()

    return render(request, 'user/login.html', {'form': form})


@login_required()
def profile_view(request):
    subject="Test"
    message="You have successfully Logged in !"
    from_email='priscillabk83@gmail.com'
    recipients=['sundasamrit40@gmail.com',]
    send_mail(subject=subject,message=message,from_email=from_email,recipient_list=recipients,fail_silently=False,)
    return render(request, 'user/profile.html')


def logout_view(request):
    logout(request)
    return redirect('/user/login/')


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            print(form.cleaned_data)

            user = USER(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],

            )
            user.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('/user/login')

    elif request.method == "GET":
        form = SignUpForm()

    return render(request, 'user/signup.html', {'form': form})
