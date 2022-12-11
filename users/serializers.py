from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phone', 'email', 'birth_day', 'gender', 'avatar', 'nationality',
                  'modified_time', 'created_time', 'is_valid')
        read_only_fields = ("id", "phone", "is_valid", "created_time", "modified_time")

    def to_representation(self, obj):
        ret = super().to_representation(obj)
        ret['gender'] = obj.get_gender_display().upper() if obj.gender else None
        ret['nationality'] = obj.get_nationality_display().upper() if obj.nationality else None
        return ret

    def update(self, instance, validated_data):
        user_email = User.objects.filter(email=validated_data.get('email')).exclude(id=instance.id).exists()
        if user_email:
            raise ValidationError("This email existed (check again) !!")
        return super(UserSerializer, self).update(instance, validated_data)


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone',)

    def create(self, validated_data):
        user = User.objects.create(phone=validated_data.get('phone'))
        return user
