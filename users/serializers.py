from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.base_address import City, Country, Location
from users.models import User, UserAddress


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ("id", 'x_coordination', 'y_coordination',)
        read_only_fields = ('id',)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name',)
        read_only_fields = ('id', 'name',)


class CitySerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True, required=False)

    class Meta:
        model = City
        fields = ('id', 'name', 'country',)
        read_only_fields = ('id',)


class AddressSerializer(serializers.ModelSerializer):
    city = CitySerializer(required=False, read_only=True)
    location = LocationSerializer(required=False, read_only=True)

    class Meta:
        model = UserAddress
        fields = ('id', 'phone', 'city', "location", 'zip_code', 'address',)
        read_only_fields = ('id', "phone",)

    def to_internal_value(self, data):
        internal_value = super(AddressSerializer, self).to_internal_value(data)
        city = data.get("city")
        if city:
            internal_value.update({
                "city": city
            })
        return internal_value

    def update(self, instance, validated_data):
        city = validated_data.pop('city')
        country = city.pop('country')
        if city:
            if country and Country.objects.filter(id=country.get('id', None)).exists():
                city_name = city.get('name', instance.city.name if instance.city else None)
                country_id = country.get('id', instance.city.country_id if instance.city else None)
                new_city, _ = City.objects.get_or_create(name=city_name,
                                                         country_id=country_id
                                                         ,
                                                         defaults={"name": city_name})
                validated_data["city"] = new_city
        super().update(instance, validated_data)
        return instance


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
