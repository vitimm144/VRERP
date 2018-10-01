from django.contrib.auth.models import User
from users.models import Career
from users.models import Employee
from users.models import BehaviorSheet
from rest_framework import viewsets
from users.serializers import UserSerializer
from users.serializers import CareerSerializer
from users.serializers import EmployeeSerializer
from users.serializers import BehaviorSheetSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().exclude(username='admin')
    serializer_class = UserSerializer


class CareerViewSet(viewsets.ModelViewSet):
    queryset = Career.objects.all()
    serializer_class = CareerSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    http_method_names = ['get', 'post', 'head', 'put', 'patch']


class BehaviorSheetViewSet(viewsets.ModelViewSet):
    queryset = BehaviorSheet.objects.all()
    serializer_class = BehaviorSheetSerializer
    http_method_names = ['get', 'post', 'head', 'put', 'patch']