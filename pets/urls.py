# from django.contrib import admin
from unicodedata import name
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

from rest_framework import routers
router = routers.DefaultRouter()
router.register('post', PetsDetailView, 'post')
router.register('wishlist', WishListDetailViews, 'wishlist')
router.register('comments', CommentDetailView, 'comments')
router.register('profile', UserProfileView, 'profile')
# router.register('filter_location', filter_data, 'filter_location')
app_name = 'pets'

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/filter_location/', filter_data_by_location, name="filter-location"),
    path('v1/search_animal/', Search_Animal, name="search-animal"),
    path('v1/search_by_category/', search_by_category_and_breed, name='search-by-category'),
    path('v1/all_district/', all_district_load, name="all-district"),
    path('v1/get_municipality/', get_municiapality, name="get-municipality"),
    path('v1/all_category/', get_all_category, name="all-category"),
    path('v1/get_pets_sold/', get_user_post_sold_unsold, name="get-pets-sold"),
    path('v1/sold_unsold_pet_detail/', get_sold_unsold_post_only, name="sold-unsold-pets-detail"),
    path('v1/api/category/<str:slug>/', get_post_by_category, name="post-by-category"),
    path('v1/get_breed_by_category/', get_breed_by_category, name="breed-by-category"),
    # path('v1/filter_by_breed/', filter_by_category_breed, name="filter-by-bread"),
    path('v1/filter_by_asc_dsc_date/', filter_by_asc_dcs_date, name="filter-by-asc-dsc-date"),
    path('v1/get_wishlist_count/', get_wishlist_count, name="get-wishlist-count")
]

