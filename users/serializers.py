from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User, Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('phone', 'country', 'city', 'zip_code', 'address',)
        read_only_fields = ("phone",)


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phone', 'email', 'birth_day', 'gender', 'avatar', 'nationality',
                  'address')
        read_only_fields = ("id", "phone",)

    def to_representation(self, obj):
        ret = super().to_representation(obj)
        ret['gender'] = obj.get_gender_display().upper() if obj.gender else None
        ret['nationality'] = obj.get_nationality_display().upper() if obj.nationality else None

        query_address = Address.objects.filter(phone=obj.phone, is_valid=True)
        ret['address'] = AddressSerializer(query_address.first()).data if query_address.exists() else None
        return ret

    def update(self, instance, validated_data):
        user_email = User.objects.filter(email=validated_data.get('email')).exclude(id=instance.id).exists()
        if user_email:
            raise ValidationError("This email existed !!")
        return super(UserSerializer, self).update(instance, validated_data)
