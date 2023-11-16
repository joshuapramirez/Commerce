from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid


def index(request):
    active_listings = Listing.objects.filter(isActive=True)
    all_categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": active_listings,
        "categories": all_categories,
    })

def show_category(request):
    if request.method == "POST":
        selected_category = request.POST.get("selected_category")  # Use get() instead of indexing
        if selected_category:
            category = Category.objects.get(categoryName=selected_category)
            active_listings = Listing.objects.filter(isActive=True, category=category)
            all_categories = Category.objects.all()
            return render(request, "auctions/index.html", {
                "listings": active_listings,
                "categories": all_categories,
            })
        else:
            return HttpResponseRedirect(reverse(index))

def createListing(request):
    if request.method == "GET":
        all_categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": all_categories
        })
    else:
        # Get data from the form
        title = request.POST["title"]
        description = request.POST["description"]
        imageurl = request.POST["imageurl"]
        price = request.POST["price"]
        category = request.POST["category"]
        # Who is the user
        current_user = request.user
        # Get all content about category
        category_data = Category.objects.get(categoryName=category)
        # Create a bid
        bid = Bid(bid=float(price), author=current_user)
        bid.save()
        # Create a new listing object
        new_listing = Listing(
            title = title,
            description = description,
            imageURL = imageurl,
            price = bid,
            category = category_data,
            owner = current_user
        )
        # Insert the obeject in our database
        new_listing.save()
        # Redirect to the index page
        return HttpResponseRedirect(reverse(index))

def listing(request, id):
    listing_details = Listing.objects.get(pk=id)
    isListingInWatchlist = request.user in listing_details.watchlist.all()
    all_comments = Comment.objects.filter(listing=listing_details)
    is_owner = request.user.username == listing_details.owner.username
    return render(request, "auctions/listing.html", {
        "details": listing_details,
        "isListingInWatchlist": isListingInWatchlist,
        "comments": all_comments,
        "is_owner": is_owner
    })

def add_bid(request, id):
    new_bid = request.POST['new_bid']
    listing_details = Listing.objects.get(pk=id)
    isListingInWatchlist = request.user in listing_details.watchlist.all()
    all_comments = Comment.objects.filter(listing=listing_details)
    is_owner = request.user.username == listing_details.owner.username

    if not listing_details.isActive:
        return render(request, "auctions/listing.html", {
            "details": listing_details,
            "message": "This auction is no longer active. Bidding is closed.",
            "update": False,
            "isListingInWatchlist": isListingInWatchlist,
            "comments": all_comments,
            "is_owner": is_owner
        })

    if float(new_bid) > listing_details.price.bid:
        updated_bid = Bid(author=request.user, bid=float(new_bid))
        updated_bid.save()
        listing_details.price = updated_bid
        listing_details.save()
        return render(request, "auctions/listing.html", {
            "details": listing_details,
            "message": "Your bid was successfully placed",
            "update": True,
            "isListingInWatchlist": isListingInWatchlist,
            "comments": all_comments,
            "is_owner": is_owner
        })
    else:
        return render(request, "auctions/listing.html", {
            "details": listing_details,
            "message": "Your bid failed to be placed",
            "update": False,
            "isListingInWatchlist": isListingInWatchlist,
            "comments": all_comments,
            "is_owner": is_owner
        })

def close_auction(request, id):
    listing_details = Listing.objects.get(pk=id)
    listing_details.isActive = False
    listing_details.save()
    is_owner = request.user.username == listing_details.owner.username
    isListingInWatchlist = request.user in listing_details.watchlist.all()
    all_comments = Comment.objects.filter(listing=listing_details)

    return render(request, "auctions/listing.html", {
        "details": listing_details,
        "isListingInWatchlist": isListingInWatchlist,
        "comments": all_comments,
        "is_owner": is_owner,
        "update": True,
        "message": "Congratulations on the successful sale! Your product has been sold at the auction.",
    })

def watchlist(request):
    current_user = request.user
    listings = current_user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

def add_watchlist(request, id):
    listing_details = Listing.objects.get(pk=id)
    current_user = request.user
    listing_details.watchlist.add(current_user)
    return HttpResponseRedirect(reverse("listing",args=(id, )))

def remove_watchlist(request, id):
    listing_details = Listing.objects.get(pk=id)
    current_user = request.user
    listing_details.watchlist.remove(current_user)
    return HttpResponseRedirect(reverse("listing",args=(id, )))


def add_comment(request, id):
    listing_details = Listing.objects.get(pk=id)
    current_user = request.user
    message = request.POST['new_comment']

    new_comment = Comment(
        author = current_user,
        listing = listing_details,
        message = message
    )

    new_comment.save()

    return HttpResponseRedirect(reverse("listing",args=(id, )))


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
