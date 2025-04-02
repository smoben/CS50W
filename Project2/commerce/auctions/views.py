from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django import forms
from .models import User, AuctionListings


class CreateForm(forms.Form):
    title = forms.CharField(label="Title of your auction", max_length=64)
    description = forms.CharField(widget=forms.Textarea, label="Your decription", max_length=100)
    bid = forms.IntegerField(label="Starting bid")
    pic_url = forms.URLField(label="Picture link (optional)", required=False)


def index(request):
    return render(request, "auctions/index.html", {
        "auctions": AuctionListings.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            title1 = form.cleaned_data["title"]
            description1 = form.cleaned_data["description"]
            bid1 = form.cleaned_data["bid"]
            pic_url1 = form.cleaned_data["pic_url"]
            a = AuctionListings(title=title1, description=description1, bid=bid1, pic_url=pic_url1)
            a.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html", {
        "form": CreateForm()
    })

def listing(request):
    return render(request, 'auctions/listing.html')