from rest_framework import serializers
from account.models import User, UserFamily
from rest_framework.authtoken.models import Token


class UserFamilySerializer(serializers.ModelSerializer):

    class Meta:
        model = UserFamily
        fields = ('id', 'name', 'age', 'aadhar', 'occupation_type', 'occupation_title')

class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ('id','first_name', 'last_name', 'email', 'phone', 'aadhar')


class UserLoginSerializer(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()

    @staticmethod
    def get_token(user):

        token, created = Token.objects.get_or_create(user=user)
        return token.key

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'role', 'token')


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "phone", "aadhar", "role")
        

class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "first_name", "middle_name", "last_name", "email", "phone", "aadhar", "country", "state", 
                "city", "constitucy", "ward", "landmark", "pincode", "gender", "date_of_birth", "role", "occupation_type", "occupation_title")

