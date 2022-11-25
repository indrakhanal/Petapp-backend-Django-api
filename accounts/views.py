import imp
from unicodedata import name
from urllib import response
from django.conf import settings

from django.shortcuts import render
# from .serializers import MyTokenObtainPairSerializer, ChangePasswordSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
# from .serializers import RegisterSerializer
from .serializers import *
from rest_framework import generics
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from accounts import serializers
from .forms import FileUploadForm
from pets.models import AnimalCategory, Location
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
User=get_user_model()
from .serializers import UserSerializer, TokenObtainPairSerializer


# class MyObtainTokenPairView(TokenObtainPairView):
#     permission_classes = (AllowAny,)
#     serializer_class = MyTokenObtainPairSerializer

#     # def post(self, request):
#     #     serializer = self.serializer_class(data=request.data)
#     #     serializer.is_valid(raise_exception=True)
#     #     return Response(serializer.data, status = status.HTTP_200_OK)


class RegisterView(generics.CreateAPIView):
    """
    User registration API
    """
    # queryset = settings.AUTH_USER_MODEL.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # try:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = {"message":"user registration successful"}
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
        # except:
        #     data = {"message":"error"}
        #     return Response(data, status=status.HTTP_201_CREATED, headers=headers)
            




# class RegisterView(APIView):
#     http_method_names = ['post']

#     def create(self, request, *args, **kwargs):
#         try:
#             serializer = self.get_serializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             self.perform_create(serializer)
#             headers = self.get_success_headers(serializer.data)
#             data = {"message":"user registration successful"}
#             return Response(data, status=status.HTTP_201_CREATED, headers=headers)
#         except:
#             data = {"message":"error"}
#             return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    # def post(self, *args, **kwargs):
    #     serializer = UserSerializer(data=self.request.data)
    #     if serializer.is_valid():
    #         get_user_model().objects.create_user(**serializer.validated_data)
    #         return Response(status=HTTP_201_CREATED)
    #     return Response(status=HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    # permission_classes = (DashboardPermissions,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.id == None:
            return Response({"error":"No user to change password please login First"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"error": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'success': 'Password updated successfully',
                'data': []
            }
            return Response(response)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    

def home_page(request):
    if request.method == "GET":
        form = FileUploadForm
        return render(request, 'index.html', {'form':form})
    else:
        import openpyxl
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_data = request.FILES['file']
            wb = openpyxl.load_workbook(file_data)
            worksheet = wb["Sheet1"]
            excel_data = list()
            for row in worksheet.iter_rows():
                row_data = list()
                for cell in row:
                    row_data.append(str(cell.value))
                excel_data.append(row_data)
            district_list = set([(x[1]) for x in excel_data[1:]])
            try:
                for district in district_list:
                    location_data = Location.objects.create(district=district)
                    location_data.save()
                return HttpResponse('district Has been saved successflly')
                # district = list(Location.objects.values('district'))
                # clean_district = [x['district'] for x in district]
            except:
                data_list = []
                for item in excel_data[1:]:
                    data_dis = {
                        item[1]:item[2]
                    }
                    data_list.append(data_dis)
                
                from collections import defaultdict
                result = defaultdict(list)

                for i in range(len(data_list)):
                    current = data_list[i]
                    for key, value in current.items():
                        result[key].append(value)
                from pets.models import Municipality
                for districts in result:
                    key = districts
                    value_list = list(set(result[districts]))
                    for i in range(len(value_list)):
                        muni_data = Municipality.objects.create(municipality=value_list[i], district=Location.objects.get(district=key))
                        muni_data.save()
                return HttpResponse('Successfully Saved to Database!!')
                # except Exception as e:
                #     return HttpResponse(e)
        else:
            return HttpResponse('Invalid Data Types')
                
        


@api_view(['GET'])
def check_username_available(request):
    """
    API to check if user name exist on current input or not.

    it will take username as parameter
    """
    name = request.GET.get('username', "")
    if len(name) >= 5:
        username = User.objects.filter(username=name).values()
        if username:
            return JsonResponse({'message':'not available'})
        else:
            return JsonResponse({'message': 'available'})
    else:
        return JsonResponse({'message': 'username should greater than 5 character'})
    # return JsonResponse()

    

def upload_category_breed(request):
    import pandas as pd
    form = FileUploadForm(request.POST, request.FILES)
    if form.is_valid():
        file_data = request.FILES['file']
        df = pd.read_csv(file_data)
        category = df["Category"].tolist()
        breed = df["Breed"].tolist()
        category_list = list(set(category))
        try:
            for cat in category_list:
                obj = AnimalCategory.objects.create(name=cat, type=cat)
                obj.save()
            return HttpResponse("Category Saved Successfully")
        except:
            data_list = []
            for i in range(len(category)):
                data_dis = {
                    category[i]:breed[i]
                }
                data_list.append(data_dis)
            from collections import defaultdict
            result = defaultdict(list)

            for i in range(len(data_list)):
                current = data_list[i]
                for key, value in current.items():
                    result[key].append(value)
            from pets.models import Breed
            for item in result:
                key = item
                values_list = list(set(result[item]))
                for i in range(len(values_list)):
                    obj = Breed.objects.create(breed=values_list[i], category=AnimalCategory.objects.get(name=key))
                    breed = values_list[i]
            return HttpResponse("Breed Saved Successfully")

    return HttpResponse("success")