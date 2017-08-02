from django.contrib.auth.models import User
from users.models import Career
from rest_framework import viewsets
from users.serializers import UserSerializer
from users.serializers import CareerSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CarrerViewSet(viewsets.ModelViewSet):
    queryset = Career.objects.all()
    serializer_class = CareerSerializer
