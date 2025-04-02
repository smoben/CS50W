from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=100)
    bid = models.IntegerField()
    pic_url = models.URLField()

    def __str__(self):
        return f"{self.id}: {self.title}"

class Bids(models.Model):
    pass

class Comments(models.Model):
    pass