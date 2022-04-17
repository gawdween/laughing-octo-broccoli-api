from rest_framework import serializers
from django.contrib.auth import get_user_model
from api.models import CustomerProfile, CustomerTransaction


User = get_user_model()

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    transactions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('id', 'email', 'is_staff', 'is_active', 'transactions')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'], validated_data['password'])

        return user


class StaffUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_staffuser(validated_data['email'], validated_data['password'])

        return user


class CustomerProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = CustomerProfile
        fields = '__all__'


class CustomerTransactionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = CustomerTransaction
        fields = '__all__'
