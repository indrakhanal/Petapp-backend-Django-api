from distutils.command.upload import upload
from unicodedata import category
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from django.conf import settings


class Location(models.Model):
    district = models.CharField(max_length=50, unique=True)
    # parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    # is_active = models.BooleanField()

    class Meta:
        verbose_name_plural = 'Locations'
        ordering = ('district',)
    
    def __str__(self):
        return self.district



class Municipality(models.Model):
    municipality = models.CharField(max_length=100)
    district = models.ForeignKey(Location, on_delete=models.CASCADE)

    class Meta:
        ordering=('municipality',)

    def __str__(self):
        return self.municipality




class AnimalCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

class Breed(models.Model):
    category = models.ForeignKey(AnimalCategory, on_delete=models.CASCADE)
    breed = models.CharField(max_length=40)

    def __str__(self):
        return self.breed

class PetDetailPost(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category_id = models.ForeignKey(AnimalCategory, on_delete=models.CASCADE)
    breed_id = models.ForeignKey(Breed, null=True, blank=True, on_delete=models.CASCADE)
    district_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    municipality_id = models.ForeignKey(Municipality, on_delete=models.CASCADE)
    user_address = models.CharField(max_length=100)
    pet_name = models.CharField(max_length=100)
    pet_age = models.CharField(max_length= 20,  null=True, blank=True)
    # user_contact = models.CharField(max_length=20)
    price = models.FloatField()
    discount = models.FloatField(null=True, blank=True)
    give_milk = models.BooleanField(default=False)
    give_milks_value = models.CharField(max_length=100, null=True, blank=True)
    discription = models.TextField(max_length=500, null=True, blank=True)
    image1 = models.ImageField(upload_to='pet_images')
    image2 = models.ImageField(upload_to='pet_images')
    image3 = models.ImageField(upload_to='pet_images', null=True, blank=True)
    image4 = models.ImageField(upload_to='pet_images', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    mark_as_sold = models.BooleanField(default=False)

    @property
    def return_absolute_url(self):
        image1 = self.image1.url
        return image1 #image2, image3, image4

    class Meta:
        verbose_name_plural = 'PetDetailPost'
        ordering = ('-id',)

    def __str__(self):
        return str(self.user_id.email)


# class WishList(models.Model):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

#     class Meta:
#         verbose_name_plural = 'Wishlists'
#         ordering = ('-id',)

#     def __str__(self):
#         return self.user.email

    # def total_count(self):
    #     return self.wish_list_items.all().count()


class WishListItem(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='wish_list_items',
                                 on_delete=models.CASCADE)
    post_id = models.ForeignKey(
        PetDetailPost, related_name='list_wish', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-id',)
        # verbose_name_plural = 'Wish List Items'

    def __str__(self):
        return self.post_id.pet_name

    @property
    def get_fabourite_count(self):
        count = self.user_id.all().count()
        return count


class Comment(models.Model):
    post = models.ForeignKey(PetDetailPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class UserProfile(models.Model):
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name  = models.CharField(max_length=20, null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # contact_no = models.CharField(null=True, blank=True, max_length=20)
    user_photo = models.ImageField(upload_to='user_photo', null=True, blank=True)
    district = models.OneToOneField(Location, null=True, blank=True, on_delete=models.CASCADE)
    municipality = models.OneToOneField(Municipality, null=True, blank=True, on_delete=models.CASCADE)
    local_address = models.CharField(max_length=100, null=True, blank=True)
    choices = models.ManyToManyField(AnimalCategory)

    def __str__(self):
        return self.user.email
