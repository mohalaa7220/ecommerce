
from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import User


# ========== Register ==========
class AdminSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'gender', 'role')
        extra_kwargs = {'password': {'write_only': True},
                        'role': {'default': 'admin'}}

    def validate(self, attrs):
        email_exits = User.objects.filter(email=attrs.get('email')).exists()
        if not attrs.get('gender'):
            raise ValidationError({"message": "gender is required"})

        if email_exits:
            raise ValidationError({"message": "email is used"})
        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class GuestSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'gender', 'role')
        extra_kwargs = {'password': {'write_only': True},
                        'role': {'default': 'guest'}}

    def validate(self, attrs):
        email_exits = User.objects.filter(email=attrs.get('email')).exists()
        if not attrs.get('gender'):
            raise ValidationError({"message": "gender is required"})

        if email_exits:
            raise ValidationError({"message": "email is used"})
        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


# ========== User Data ==========
class UserDataSerializer(serializers.ModelSerializer):

    join_date = serializers.DateTimeField(source='formatted_date_joined')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'is_staff',
                  'gender', 'join_date')


# ============================================================================
# Reset Password
# ============================================================================
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs["email"]).exists()
        if email_exists == False:
            raise ValidationError({"message": "Email does not exist"})
        return super().validate(attrs)


class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs["email"]).exists()
        if email_exists == False:
            raise ValidationError({"message": "Email does not exist"})
        return super().validate(attrs)


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8)
    email = serializers.EmailField()

    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs["email"]).exists()
        if email_exists == False:
            raise ValidationError({"message": "Email does not exist"})
        return super().validate(attrs)
