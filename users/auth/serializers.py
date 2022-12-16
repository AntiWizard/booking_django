from rest_framework import serializers

from users.models import User


class OTPSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=5)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone',)

    def create(self, validated_data):
        user = User.objects.create(phone=validated_data.get('phone'))
        return user
