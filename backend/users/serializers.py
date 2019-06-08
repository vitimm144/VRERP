from django.conf.urls import url, include
from django.db import transaction, IntegrityError
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from users.models import Career
from users.models import Employee
from users.models import BehaviorSheet
from users.models import WorkSchedule
from users.models import WorkShift
from pprint import pprint


# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'is_staff',
            'is_active',
            'password',

        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            is_staff=validated_data['is_staff'],
            is_active=validated_data['is_active'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        pprint(validated_data)
        for attr, value in validated_data.items():
            if attr == 'password':
                continue
            setattr(instance, attr, value)

        if validated_data.get('password'):
            instance.set_password(validated_data['password'])
        instance.save()
        return instance


class CareerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Career
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class BehaviorSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = BehaviorSheet
        fields = '__all__'


class WorkShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkShift
        fields = '__all__'


class WorkScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkSchedule
        fields = (
            'id',
            'month',
            'year',
            'shift_start',
            'shift_end',
            'employee',
            'employee_name',
        )

    # def create(self, validated_data):
    #     return self.create_update(None, validated_data)
    #
    # def update(self, instance, validated_data):
    #     return self.create_update(instance, validated_data)
    #
    # def create_update(self, instance, validated_data):
    #     work_shifts = validated_data.pop('work_shifts', None)
    #
    #     if not instance:
    #         instance = super(WorkScheduleSerializer, self).create(validated_data)
    #     else:
    #         for attr, value in validated_data.items():
    #             setattr(instance, attr, value)
    #
    #     if work_shifts:
    #         with transaction.atomic():
    #             ids = []
    #             for x in work_shifts:
    #                 identifier = x.get('id')
    #                 if identifier:
    #                     ids.append(identifier)
    #             instance.work_shifts.exclude(pk__in=ids).delete()
    #
    #             for work_shift in work_shifts:
    #                 if not work_shift.get('id'):
    #                     WorkShift.objects.create(
    #                         work_schedule=instance,
    #                         **work_shift
    #                     )
    #                 else:
    #                     edited_work_shift = WorkShift.objects.get(pk=work_shift.get('id'))
    #                     for attr, value in work_shift.items():
    #                         setattr(edited_work_shift, attr, value)
    #                         edited_work_shift.save()
    #
    #     instance.save()
    #
    #     return instance
