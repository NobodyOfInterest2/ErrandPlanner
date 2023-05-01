from django.urls import reverse
from django.shortcuts import render, redirect
from . import models, utils
from app.forms import ErrandForm
from django.contrib.auth.models import User
from django.contrib import messages
from authlib.integrations.django_client import OAuth
from functools import wraps
import os, datetime

# Create your views here.

AUTH_REDIRECT_URI = os.getenv("AUTH_REDIRECT_URI")
print(AUTH_REDIRECT_URI)

CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"
oauth = OAuth()
oauth.register(
    name="google",
    server_metadata_url=CONF_URL,
    client_kwargs={
        "scope": "openid email profile  https://www.googleapis.com/auth/calendar.events  https://www.googleapis.com/auth/calendar.readonly"
    },
)


# Function decorator that checks whether there is an active user
def auth_required(func):
    @wraps(func)
    def wrapper(request):
        user = request.session.get("user")
        if user:
            return func(request)
        else:
            return redirect("/login")

    return wrapper


def login(request):
    redirect_uri = str(AUTH_REDIRECT_URI)
    return oauth.google.authorize_redirect(request, redirect_uri)


def logout(request):
    request.session.flush()
    return redirect("/")


def auth(request):
    token = oauth.google.authorize_access_token(request)
    request.session["user"] = token["userinfo"]
    request.session["token"] = token
    return redirect("/")


## Errand Views ##


@auth_required
def errands(request):
    # Simply load errands for rendering
    email = request.session.get("user")["email"]
    table_data = models.Event.objects.filter(user=email)
    context = {"table_data": table_data}
    return render(request, "errands.html", context)


@auth_required
def deleteErrand(request, pk):
    prod = models.Event.objects.get(id=pk)
    prod.delete()
    messages.success(request, "errand deleted successfully")
    return redirect("/errands")


# Add errand
@auth_required
def addErrand(request):
    if request.method == "POST":
        if "add" in request.POST:
            # User has added an errand
            add_form = ErrandForm(request.POST)
            if add_form.is_valid():
                title = add_form.cleaned_data["title"]
                priority = add_form.cleaned_data["priority"]
                streetaddr = add_form.cleaned_data["streetaddr"]
                city = add_form.cleaned_data["city"]
                state = add_form.cleaned_data["state"]
                zip = add_form.cleaned_data["zip"]
                duration = add_form.cleaned_data["duration"]
                user = request.session.get("user")["email"]
                models.Event(
                    user=user,
                    title=title,
                    priority=priority,
                    streetaddr=streetaddr,
                    city=city,
                    state=state,
                    zip=zip,
                    duration=duration,
                    scheduled=False,
                ).save()
                return redirect("/errands/")
            else:
                context = {"form_data": add_form}
                return render(request, "addErrand.html", context)
        else:
            # Cancel
            return redirect("/errands/")
    else:
        context = {"form_data": ErrandForm()}
    return render(request, "addErrand.html", context)


@auth_required
def editErrand(request, id):
    if request.method == "GET":
        # Load Errand Entry Form with current model data.
        errand = models.Event.objects.get(id=id)
        form = ErrandForm(instance=errand)
        context = {"form_data": form}
        return render(request, "editErrand.html", context)
    elif request.method == "POST":
        # Process form submission
        if "edit" in request.POST:
            form = ErrandForm(request.POST)
            if form.is_valid():
                errand = form.save(commit=False)
                errand.user = request.user
                errand.id = id
                errand.scheduled = False
                errand.save()
                return redirect("/errands/")
            else:
                context = {"form_data": form}
                return render(request, "addErrand.html", context)
        else:
            # Cancel
            return redirect("/errands/")
