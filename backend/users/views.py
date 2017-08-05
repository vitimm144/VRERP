from django.contrib.auth.models import User
from users.models import Career
from users.models import Employee
from rest_framework import viewsets
from users.serializers import UserSerializer
from users.serializers import CareerSerializer
from users.serializers import EmployeeSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CareerViewSet(viewsets.ModelViewSet):
    queryset = Career.objects.all()
    serializer_class = CareerSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    http_method_names = ['get', 'post', 'head', 'put', 'patch']
