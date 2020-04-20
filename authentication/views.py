"""
views for authentication
"""

from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login
from django.views import generic
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from .models import User
from .forms import EditEmailForm, EditPhoneNumberForm, EditName


@login_required
def login_redirect(request):
    """
    function to redirect user after login
    """
    return redirect(reverse("profile", args=(request.user.id,)))


def register(request):
    """
    view to handle users registration
    """
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect(reverse('profile', args=(user.id,)))
    else:
        form = RegistrationForm()

    context = {'form':form}

    return render(request, 'registration/register.html', context=context)



class ProfileView(generic.DetailView):
    """
    profile view
    """
    model = User
    template_name = "registration/profile.html"
    context_object_name = "user"


@login_required()
def edit_email_view(request):
    """
    edit email view
    """
    if request.method == "GET":
        form = EditEmailForm()
        return render(request, 'profile_editing/edit_email.html', {"form":form})

    elif request.method == "POST":
        form = EditEmailForm(request.POST)
        if form.is_valid():
            new_email = form.cleaned_data['email']
            user = User.objects.get(email=request.user.email)
            user.email = new_email
            user.save()
            return redirect(reverse("profile", args=(request.user.id,)))
        return render(request, "profile_editing/edit_email.html", {"form":form})



@login_required()
def edit_phone_view(request):
    """
    edit phone number view
    """
    if request.method == "GET":
        form = EditPhoneNumberForm()
        return render(request, 'profile_editing/add_or_edit_phone.html', {"form":form})

    elif request.method == "POST":
        form = EditPhoneNumberForm(request.POST)
        if form.is_valid():
            new_phone = form.cleaned_data['phone']
            user = User.objects.get(email=request.user.email)
            user.phone = new_phone
            user.save()
            return redirect(reverse("profile", args=(request.user.id,)))
        return render(request, "profile_editing/add_or_edit_phone.html", {"form":form})


@login_required()
def edit_name_view(request):
    """
    edit name view
    """
    if request.method == "GET":
        form = EditName()
        return render(request, 'profile_editing/add_or_edit_name.html', {"form":form})

    elif request.method == "POST":
        form = EditName(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            user = User.objects.get(email=request.user.email)
            user.name = name
            user.save()
            return redirect(reverse("profile", args=(request.user.id,)))
        return render(request, "profile_editing/add_or_edit_name.html", {"form":form})



