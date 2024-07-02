from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm


def homePage(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            return HttpResponse("Logged in!")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# def forgot_password_view(request):
#     return HttpResponse("Forgot password page")
# Create your views here.


from django.shortcuts import render
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect

def forgot_password_view(request):
    if request.method == 'POST':
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': get_current_site(request).domain,
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_email = EmailMessage(subject, email, to=[user.email])
                        send_email.send()
                    except Exception as e:
                        return HttpResponseRedirect('/email-not-sent/')
            return HttpResponseRedirect('/password-reset-done/')
    password_reset_form = PasswordResetForm()
    return render(request, 'forgot_password.html', {'password_reset_form': password_reset_form})

from django.shortcuts import render

def password_reset_done(request):
    return render(request, 'password_reset_done.html')
