from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from .forms import LoginForm


class CustomLogoutView(LogoutView):
    http_method_names = ['get', 'post']

def custom_logout(request):
    request.session.flush()
    return CustomLogoutView.as_view()(request)

