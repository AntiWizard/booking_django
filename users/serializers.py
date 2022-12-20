from rest_framework import serializers
from rest_framework.exceptions import ValidationError

# from sub_models.location import Location
from users.models import User, UserAddress


# class LocationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Location
#         fields = ("id", 'x_coordination', 'y_coordination',)
#         read_only_fields = ('id',)


class AddressSerializer(serializers.ModelSerializer):
    # location = LocationSerializer(required=False, read_only=True)

    class Meta:
        model = UserAddress
        fields = ('id', 'phone', "country", 'city', "location", 'zip_code', 'address',)
        read_only_fields = ('id', "phone",)


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

        query_address = UserAddress.objects.filter(phone=obj.phone)
        ret['address'] = AddressSerializer(query_address.first()).data if query_address.exists() else None
        return ret

    def update(self, instance, validated_data):
        user_email = User.objects.filter(email=validated_data.get('email')).exclude(id=instance.id).exists()
        if user_email:
            raise ValidationError("This email existed !!")
        return super(UserSerializer, self).update(instance, validated_data)
