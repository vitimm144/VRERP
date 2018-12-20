from django.contrib.auth.models import User
from users.models import Career
from users.models import Employee
from users.models import BehaviorSheet
from users.models import WorkSchedule
from users.models import WorkShift
from rest_framework import viewsets
from users.serializers import UserSerializer
from users.serializers import CareerSerializer
from users.serializers import EmployeeSerializer
from users.serializers import BehaviorSheetSerializer
from users.serializers import WorkScheduleSerializer
from users.serializers import WorkShiftSerializer
import django_filters.rest_framework


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().exclude(username='admin')
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'head', 'put', 'patch']
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('email', 'username',)


class CareerViewSet(viewsets.ModelViewSet):
    queryset = Career.objects.all()
    serializer_class = CareerSerializer
    http_method_names = ['get', 'post', 'head', 'put', 'patch']
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('title',)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    http_method_names = ['get', 'post', 'head', 'put', 'patch']
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('cpf', 'rg', 'code', 'career',)


class BehaviorSheetViewSet(viewsets.ModelViewSet):
    queryset = BehaviorSheet.objects.all()
    serializer_class = BehaviorSheetSerializer
    http_method_names = ['get', 'post', 'head', 'put', 'patch']
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('employee', 'behavior_type')


class WorkScheduleViewSet(viewsets.ModelViewSet):
    queryset = WorkSchedule.objects.all()
    serializer_class = WorkScheduleSerializer
    http_method_names = ['get', 'post', 'head', 'put', 'patch']
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('employee',)


class WorkShiftViewSet(viewsets.ModelViewSet):
    queryset = WorkShift.objects.all()
    serializer_class = WorkShiftSerializer
    http_method_names = ['get', 'post', 'head', 'put', 'patch']
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('work_schedule',)
