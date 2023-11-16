from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName = models.CharField(max_length=50)

    def __str__(self):
        return self.categoryName


class Bid(models.Model):
    bid = models.FloatField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_bid")


class Listing(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    imageURL = models.CharField(max_length=1000)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="price")
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlist")

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_comment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, related_name="listing_comment")
    message = models.CharField(max_length=200)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.author} comment on {self.listing}"