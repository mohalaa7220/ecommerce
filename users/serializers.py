
from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import User


# ========== Register ==========
class UserBaseRegistration(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'gender', 'role')

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


# ============== Admin Register =================
class AdminSignUpSerializer(UserBaseRegistration):
    class Meta(UserBaseRegistration.Meta):
        fields = UserBaseRegistration.Meta.fields
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'default': 'admin'},
            'is_staff': True, 'is_superuser': True
        }


# ============== Guest Register =================
class GuestSignUpSerializer(UserBaseRegistration):
    class Meta(UserBaseRegistration.Meta):
        fields = UserBaseRegistration.Meta.fields
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'default': 'guest'}
        }


# ========== User Data ==========
class UserDataSerializer(serializers.ModelSerializer):

    join_date = serializers.DateTimeField(source='formatted_date_joined')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'is_staff', 'is_superuser',
                  'gender', 'join_date')


# ============================================================================
# Reset Password
# ============================================================================
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get("email")

        if not email:
            raise ValidationError({"message": "Email is required"})

        if not User.objects.filter(email=email).exists():
            raise ValidationError({"message": "Email does not exist"})

        return attrs


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
