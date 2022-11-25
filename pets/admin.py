from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register([Location, Municipality, AnimalCategory, PetDetailPost, WishListItem, Comment, UserProfile, Breed])
