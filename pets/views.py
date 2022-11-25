from unicodedata import category
from urllib import response
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import PetsPostSerializers, UserProfileSerializers, WishListSearializers, CommentSerializers
from .models import AnimalCategory, Breed, Location, Municipality, PetDetailPost, UserProfile, WishListItem, Comment
from django.db.models import Q
from rest_framework import status
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
# from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from .permissions import IsAuthenticated


class PetsDetailView(viewsets.ModelViewSet):
    """
    API for main post that user will create.
    """
    fields = '__all__'
    serializer_class = PetsPostSerializers
    queryset = PetDetailPost.objects.all()
    permission_classes = (IsAuthenticated,)
    def create(self, request, *args, **kwargs):
        # try:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = {"message":"success"}
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
        # except:
        #     data={"message":"error"}
        #     return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        category = AnimalCategory.objects.values_list('id')
        try:
            user=get_object_or_404(User, id=request.user.id)
            data = {}
            if user:
                """
                if user is logged in
                """
                user_address = list(UserProfile.objects.filter(user=user).values('district', 'municipality', 'local_address'))
                district = user_address[0]['district']
                municipality = user_address[0]['municipality']
                local_address = user_address[0]['local_address']
                queryset = PetDetailPost.objects.filter(Q(district_id=district)| Q(municipality_id=municipality)| Q(user_address__icontains=local_address), mark_as_sold=False).values()
                if queryset:
                    data["nearrest_animal"]=queryset
                    # qs_list.append({
                    #     "nearest_animal":queryset
                    # })
                choices = UserProfile.objects.filter(user=user).values_list("choices")
                qs_list =[]
                for i in choices:
                    name = AnimalCategory.objects.filter(id=i[0]).values("name")[0]['name']
                    post = PetDetailPost.objects.filter(category_id__id=i[0], mark_as_sold=False).values()
                    if post and name:
                        qs_list.append({
                            name:post
                        })
                data["choices_animal"]=qs_list
                    
                not_in_choices = [x for x in category if x not in choices]
                not_choices = []
                for item in not_in_choices:
                    qs = PetDetailPost.objects.filter(category_id=item, mark_as_sold=False).values()
                    cat_name = AnimalCategory.objects.filter(id=item[0]).values('name')[0]['name']
                    if qs and cat_name:
                        not_choices.append({
                            cat_name:qs
                        })
                not_choices = list(not_choices)
                data["not_in_choices"]=not_choices
                return Response(data, status=status.HTTP_200_OK)
        except:
            """
            if user is not logged in
            """
            queryset = PetDetailPost.objects.all()
            qs_list =[]
            for item in category:
                qs = queryset.filter(category_id=item).values()
                cat_name = AnimalCategory.objects.filter(id=item[0]).values('name')[0]['name']
                qs_list.append({
                    cat_name:qs
                })
            qs_list.append({"message":"create your profile to see post near your location"})
            return Response(qs_list, status=status.HTTP_200_OK)
       
    
    def retrieve(self, request, *args, **kwargs):
        from django.db.models import F
        instance = self.get_object()
        qs = PetDetailPost.objects.filter(id=instance.id).values()
        qs = qs.values("user_id","user_address", "pet_name", "pet_age", "price", "discount","give_milk", "give_milks_value",
                    "discription", "image1", "image2", "image3", "image4", "created_on", "mark_as_sold",contact_no=F("user_id__phone"), 
                    district_name=F("district_id__district"),municipality_name=F("municipality_id__municipality"), category_name=F("category_id__name"))
        return Response(qs, status=status.HTTP_200_OK)


class WishListDetailViews(viewsets.ModelViewSet):
    """
    API for marking post as  favourite 
    """
    fields = '__all__'
    serializer_class = WishListSearializers
    queryset = WishListItem.objects.all()
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            data = {"message":"success"}
            return Response(data, status=status.HTTP_201_CREATED, headers=headers)
        except:
            data={"message":"error"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        try:
            user = get_object_or_404(id=request.user.id)
            if user:
                wish_list = WishListItem.objects.filter(user_id=user).values()
                return Response(wish_list, status=status.HTTP_200_OK)
            else:
                return Response({"message":"whishlist is empty"}, status=status.HTTP_200_OK)
        except:
            return Response({"message":"authentication failed"}, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(viewsets.ModelViewSet):
    """
    API for add comment
    """
    fields = '__all__'
    serializer_class =  CommentSerializers
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticated,)


    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            data = {"message":"success"}
            return Response(data, status=status.HTTP_201_CREATED, headers=headers)
        except:
            data={"message":"error"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(viewsets.ModelViewSet):
    """
    API for User Profile 
    """
    fields = '__all__'
    serializer_class = UserProfileSerializers
    queryset = UserProfile.objects.all()
    permission_classes = (IsAuthenticated,)


    def create(self, request, *args, **kwargs):
        """
        Profile create API
        """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            data = {"message":"success profile created"}
            return Response(data, status=status.HTTP_201_CREATED, headers=headers)
        except:
            data={"message":"error"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        """
        Get user profile data API
        """
        # try:
        user=get_object_or_404(User, id=request.user.id)
        if user:
            data = UserProfile.objects.filter(user=user).values()
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"message":"user not found"}, status=status.HTTP_200_OK)
        # except:
        #     return Response({"message":"authentication failed!"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_post_by_category(request, slug):
    try:
        user = get_object_or_404(User, id=request.user.id)
        if user.id !=None:
            user_address = list(UserProfile.objects.filter(user=user).values('district', 'municipality', 'local_address'))
            if user_address:
                district = user_address[0]['district']
                municipality = user_address[0]['municipality']
                local_address = user_address[0]['local_address']
                queryset = PetDetailPost.objects.filter(Q(district_id=district)| Q(municipality_id=municipality)| Q(user_address__icontains=local_address), mark_as_sold=False).values()
                qs  = queryset.filter(category_id__name__icontains=slug)
                if not qs:
                    qs = PetDetailPost.objects.filter(category_id__name__icontains=slug)
                data ={
                    slug:qs
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                qs = PetDetailPost.objects.filter(category_id__name=slug).values()
                data ={
                    slug:qs,
                    "message":"Update your profile to see the post near you"
                }
                return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"error":"UnAuthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    except:
        qs = PetDetailPost.objects.filter(category_id__name=slug).values()
        data ={
            slug:qs,
        }
        return Response(data, status=status.HTTP_200_OK)


    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_post_sold_unsold(request, format=None):
    """
    This Api will get total post by user, total sold post, total unsold post

    for example the response will like below:
                'sold_post':10,
                'unsold_post':20,
                'total_post':30
    """
    try:
        # from django.db.models import Count
        user = PetDetailPost.objects.filter(user_id =request.user)
        if user:
            sold_post = PetDetailPost.objects.filter(user_id=request.user, mark_as_sold=True).values().count()
            unsold_post = PetDetailPost.objects.filter(user_id=request.user, mark_as_sold=False).values().count()
            total_post = sold_post+unsold_post
            data = {
                'sold_post':sold_post,
                'unsold_post':unsold_post,
                'total_post':total_post
            }
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response({"message":"User has no post Yet"})
    except:
        return Response({"message":"authentication failed!"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_sold_unsold_post_only(request, format=None):
    """
    This API return post detail of sold post and unsold post.
    """
    try:
        user=PetDetailPost.objects.filter(user_id=request.user)
        if user:
            sold_post = PetDetailPost.objects.filter(user_id=request.user, mark_as_sold=True).values()
            unsold_post =PetDetailPost.objects.filter(user_id=request.user, mark_as_sold =False).values()
            return JsonResponse({'sold_post':list(sold_post), 'unsold_post':list(unsold_post)})
        else:
            return Response({"message":"user has no any post yet"})
    except:
        return Response({"message":"Not Authenticate"})
    

@api_view(['GET'])
def filter_data_by_location(request, format=None):
    """ 
    API for filtering data by location 
    it will take three parameter to filter the post
    'district', 'municiapality', 'location'
    request parameter look like::
    /api/v1/filter_location/?district=1&municiapality=1&location=samakhusi

    """
    district = request.GET.get('district')
    municipality = request.GET.get('municiapality')
    location = request.GET.get('location')
    queryset = PetDetailPost.objects.filter(district_id=district, municipality_id=municipality, user_address=location, marked_as_sold=False).values()
    return Response(queryset)
    # return response.Ok(yourData)

@api_view(['GET'])
def Search_Animal(request, format=None):
    """
    API for serching animal by pet name or pet description

    it will take one key name 'pet_name'  
    request parameter look like :: /api/v1/search_animal/?pet_name=buffallow
    """
    pet_name = request.GET.get('pet_name', '')
    pets = PetDetailPost.objects.filter(Q(pet_name__icontains=pet_name) | Q(discription__icontains=pet_name), mark_as_sold=False).values()
    return Response(pets)


@api_view(['GET'])
def search_by_category_and_breed(request, format=None):
    """
    API for searching animal by pet category or breed
    user can choose multiple breed to search.
    it will take a key name 'category' and 'breed'
    request parameter look like
    /api/v1/search_by_category/?category=1&breed=1&breed=2&breed=3
    """
    category  = request.GET.get('category', "")
    breeds = request.GET.getlist('breed', None)
    pets = PetDetailPost.objects.filter(category_id__id=category, breed_id__in=breeds).values()
    return Response(pets)


@api_view(['GET'])
def all_district_load(request, format=None):
    """
    API for retrive all district 
    """
    district = Location.objects.all().order_by('district').values('id', 'district')
    return Response(district)


@api_view(['GET'])
def get_municiapality(request, format=None):
    """
    API for retrive all municiapility list by district

    it will take district_id as a parameter

    /v1/get_municipality/?district=1
    """
    district_id  = request.GET.get('district')
    qs = Municipality.objects.filter(district_id = district_id).order_by("municipality").values()
    return Response(qs)


@api_view(['GET'])
def get_all_category(request, format=None):
    """
    API to return all list of category
    """
    qs = AnimalCategory.objects.all().order_by("name").values()
    return Response(qs)


@api_view(['GET'])
def get_breed_by_category(request, format=None):
    """
    API to return breed of specific category if breed exists

     it will take category_id as a parameter

    /v1/get_breed_by_category/?category=1
    """
    category_id = request.GET.get("category")
    qs = Breed.objects.filter(category=category_id).values("id", "breed")
    return Response(qs)


# @api_view(['GET'])
# def filter_by_category_breed(request):
#     pass



@api_view(['Get'])
def filter_by_asc_dcs_date(request):
    """
    API to return data based on ascending descending or latest first or oldest first
    the request parameter is
    if ascending:
    v1/filter_by_asc_dsc_date/?filter=asc
    if descending:
    v1/filter_by_asc_dsc_date/?filter=dsc
    if newest first:
    v1/filter_by_asc_dsc_date/?filter=new
    if oldest first:
    v1/filter_by_asc_dsc_date/?filter=old
    """
    filter = request.GET.get("filter")
    if filter == "asc":
        qs = PetDetailPost.objects.filter(mark_as_sold=False).order_by("pet_name").values()
    elif filter == "dsc":
        qs = PetDetailPost.objects.filter(mark_as_sold=False).order_by("-pet_name").values()
    elif filter == "new":
        qs = PetDetailPost.objects.filter(mark_as_sold=False).order_by("id").values()
    elif filter == "old":
        qs = PetDetailPost.objects.filter(mark_as_sold=False).order_by("-id").values()
    return Response(qs, status=status.HTTP_200_OK)


@api_view(['Get'])
@permission_classes([IsAuthenticated])
def get_wishlist_count(request):
    """
    API to get a count number of wishlist of every user
    """
    user = get_object_or_404(User, id=request.user.id)
    print(user)
    count = WishListItem.objects.filter(user_id=user).values().count()
    print(count)
    data = {
        "wish_count":count
    }
    return Response(data=data, status=status.HTTP_200_OK)