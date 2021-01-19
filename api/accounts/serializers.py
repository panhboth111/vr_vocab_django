from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    is_active = serializers.BooleanField()
    class Meta:
        model = User
        fields = ('id','username', 'password',  'email','is_active')

    def validate(self, attrs):
        if not attrs['is_active']:
            raise serializers.ValidationError({"active": "Account's email needs to be confirmed"}) 
        return attrs
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )      
        user.set_password(validated_data['password'])
        user.save()

        return user