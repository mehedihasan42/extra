from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username','first_name','last_name','email','password','phone','present_address','hometown']
        extra_kwargs = {
            'password': {'write_only': True}
        }

        def create(self,validate_data):
            password = validate_data.pop('password')
            user = Users(**validate_data)
            user.set_password(password)
            user.save()
            return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'   
        read_only_fields = ['user']     
