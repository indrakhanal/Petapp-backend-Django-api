from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .serializers import TodoSerializers
from .models import Todo
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView



class TodoView(viewsets.ModelViewSet):
    fields = '__all__'
    serializer_class = TodoSerializers
    queryset = Todo.objects.all()
    


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

