from account.serializers import UserSerializer, UserLoginSerializer, UserDetailsSerializer, UserListSerializer, UserFamilySerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from account.models import User, UserFamily
from rest_framework.status import (HTTP_302_FOUND,
	HTTP_400_BAD_REQUEST, 
	HTTP_404_NOT_FOUND, 
	HTTP_200_OK,
	HTTP_201_CREATED,
	HTTP_204_NO_CONTENT
)
from django.db import transaction
import json
import requests
import random
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

url = "http://127.0.0.1:8080/"
def GetCountryName(country_id):
	res = requests.get(url + "country/getcountry/" + str(country_id) + "/")
	data = json.loads(res.text)
	return data["country"]["name"]

def GetStateName(state_id):
	res = requests.get(url + "country/getstate/" + str(state_id) + "/")
	data = json.loads(res.text)
	return data["state"]["name"]

def GetCityName(city_id):
	res = requests.get(url + "country/getcity/" + str(city_id) + "/")
	data = json.loads(res.text)
	return data["city"]["name"]

def GetConstitucyName(constitucy_id):
	res = requests.get(url + "country/getconstitucy/" + str(constitucy_id) + "/")
	data = json.loads(res.text)
	return data["constitucy"]["name"]


class RegisterUser(APIView):

	permission_classes = (AllowAny,)

	class UserCreateSerializer(serializers.ModelSerializer):

		class Meta:
			model = User
			fields = ("first_name", "middle_name", "last_name", "email", "phone", "aadhar", "country", "state", 
				"city", "ward", "constitucy", "gender", "date_of_birth", "role", "occupation_type", "occupation_title")

	@transaction.atomic
	def post(self, request):

		parameter_missing = False
		parameter_missing_name = ""
		if request.data.get("first_name") is None or request.data.get("first_name") == "":
			parameter_missing_name = parameter_missing_name + "first_name, "
			parameter_missing = True
		elif request.data.get("last_name") is None or request.data.get("last_name") == "":
			parameter_missing_name = parameter_missing_name + "last_name, "
			parameter_missing = True
		elif request.data.get("email") is None or request.data.get("email") == "":
			parameter_missing_name = parameter_missing_name + "email, "
			parameter_missing = True
		elif request.data.get("phone") is None or request.data.get("phone") == "":
			parameter_missing_name = parameter_missing_name + "phone, "
			parameter_missing = True
		elif request.data.get("aadhar") is None or request.data.get("aadhar") == "":
			parameter_missing_name = parameter_missing_name + "aadhar, "
			parameter_missing = True

		if parameter_missing:
			return Response({"status": False, "status_code": HTTP_204_NO_CONTENT, "message": parameter_missing_name + " missing"})

		existed_user_email = User.objects.filter(email=request.data.get("email")).first()
		if existed_user_email is None:

			existed_user_phone = User.objects.filter(phone=request.data.get("phone")).first()
			if existed_user_phone is None:

				existed_user_aadhar = User.objects.filter(aadhar=request.data.get("aadhar")).first()
				if existed_user_aadhar is None:
	
					user = User()
					user.first_name = request.data.get("first_name")
					user.middle_name = request.data.get("middle_name")
					user.last_name = request.data.get("last_name")
					user.email = request.data.get("email")
					user.phone = request.data.get("phone")
					user.aadhar = request.data.get("aadhar")
					user.country = request.data.get("country")
					user.state = request.data.get("state")
					user.city = request.data.get("city")
					user.constitucy = request.data.get("constitucy")
					user.ward = request.data.get("ward")
					user.landmark = request.data.get("landmark")
					user.pincode = request.data.get("pincode")
					user.gender = request.data.get("gender")
					user.date_of_birth = request.data.get("date_of_birth")
					user.role = "member"
					user.occupation_type = request.data.get("occupation_type")
					user.occupation_title = request.data.get("occupation_title")
					user.save()

					return Response({
						"status": True, 
						"status_code" : HTTP_200_OK, 
						"message":"User Created.", 
						"user": UserSerializer(user).data
						})
				else:
					return Response({"status":False, "status_code":HTTP_302_FOUND, "message":"Aadhar Exist."})
			else:
				return Response({"status":False, "status_code":HTTP_302_FOUND, "message":"Phone Exist."})
		else:
				return Response({"status":False, "status_code":HTTP_302_FOUND, "message":"Email Exist."})


class AddUserFamily(APIView):

	permission_classes = (AllowAny,)

	user_id = serializers.CharField(max_length=200)

	def post(self, request, *args, **kwargs):

		userId = request.data.get("user_id")

		user = User.objects.filter(id=userId).first()
	
		if user is not None:

			user_family = UserFamily()
			user_family.name = request.data.get("name")
			user_family.age = request.data.get("age")
			user_family.occupation_type = request.data.get("occupation_type")
			user_family.occupation_title = request.data.get("occupation_title")
			user_family.aadhar = request.data.get("aadhar")
			user_family.user = user
			user_family.save()

			return Response({"status" : True, "status_code": HTTP_201_CREATED, "message" : "User family member recorded successfully."})
		
		else:
			return Response({"status" : False, "status_code": HTTP_404_NOT_FOUND, "message" : "User does not exist."})


class SendOTP(APIView):

	permission_classes = (AllowAny,)

	class SendOTPSerializer(serializers.ModelSerializer):
		class Meta:

			model = User
			fields = ("aadhar")
			
	def put(self, request):

		aadhar = request.data.get("aadhar")
		otpString = random.randint(1000000,9999999)
		
		user = User.objects.filter(aadhar=aadhar).first()

		if user is not None:
			
			user.otp = otpString
			user.save()

			user_dict = {}
			user_dict["user_id"] = user.id
			user_dict["otp"] = otpString

			# reqUrl = 'https://www.sms4india.com/api/v1/sendCampaign'
			# req_params = {
			# 'apikey':'9MQTVC4LEXQEXN5MVNQX04TAHD967WCQ',
			# 'secret':'K4AA3OPX9CG5RV3U',
			# 'usetype':'stage',
			# 'phone': user.phone,
			# 'message':'Your OTP is ' + str(otpString) + ' for your ' + str(user.aadhar) + ' aadhar number login credential',
			# 'senderid':'9657445206'
			# }
			# requests.post(reqUrl, req_params)

			return Response({
								"status":True, "status_code" : HTTP_200_OK, 
								"message" : "OTP sent successfully.", "user" : user_dict
							})
		else:
			return Response({
								"status":False, "status_code" : HTTP_404_NOT_FOUND, 
								"message" : "Aadhar does not exist"
							})


class Login(APIView):

	permission_classes = (AllowAny,)

	def post(self, request):

		user_id = request.data.get('user_id')
		otp = request.data.get('otp')

		user = User.objects.filter(id=user_id, otp=otp).first()

		if user:
			serializer = UserLoginSerializer(user)
			return Response({"status": True, "status_code" : HTTP_200_OK, "user": serializer.data})

		else:
			return Response({"status":False, "status_code" : HTTP_404_NOT_FOUND, "message" : "OTP does not match."})


class Logout(APIView):

    def get(self, request):
    	token = get_object_or_404(Token, key=request.auth)
    	token.delete()
    	return Response({"status":True, "status_code":HTTP_204_NO_CONTENT, "message":"User Logout Successfully."})

class Users(APIView):

	def get(self, request, *args, **kwargs):

		role = request.user.role
		
		if role == "admin":

			users = User.objects.all()
			return Response({
				"status":True, 
				"status_code" : HTTP_200_OK, 
				"users":UserListSerializer(users, many=True).data
				})

			# users = User.objects.all()
			# paginator = PageNumberPagination()
			# context = paginator.paginate_queryset(users, request)
			# serializer = UserListSerializer(context, many=True)
			# return paginator.get_paginated_response(serializer.data)

		if role == "country head":

			users = User.objects.all().filter(Q(role="country head")|Q(role="state head")|Q(role="city head")|Q(role="constitucy head")|
				Q(role="ward head")|Q(role="branch head")|Q(role='member'))
			return Response({
					"status":True, 
					"status_code" : HTTP_200_OK, 
					"users":UserListSerializer(users, many=True).data
					})

		if role == "state head":

			users = User.objects.filter(Q(role="state head")|Q(role="city head")|Q(role="constitucy head")|
				Q(role="ward head")|Q(role="branch head")|Q(role='member'))
			return Response({
					"status":True, 
					"status_code" : HTTP_200_OK, 
					"users":UserListSerializer(users, many=True).data
					})

		if role == "city head":

			users = User.objects.filter(Q(role="city head")|Q(role="constitucy head")|
				Q(role="ward head")|Q(role="branch head")|Q(role='member'))
			return Response({
				"status":True, 
				"status_code" : HTTP_200_OK, 
				"users":UserListSerializer(users, many=True).data
				})

		if role == "constitucy head":

			users = User.objects.filter(Q(role="constitucy head")|Q(role="ward head")|Q(role="branch head")|
				Q(role='member'))
			return Response({
				"status":True, 
				"status_code" : HTTP_200_OK, 
				"users":UserListSerializer(users, many=True).data
				})

		if role == "ward head":

			users = User.objects.filter(Q(role="ward head")|Q(role="branch head")|Q(role='member'))
			return Response({
				"status":True, 
				"status_code" : HTTP_200_OK, 
				"users":UserListSerializer(users, many=True).data
				})

		if role == "branch head":

			users = User.objects.filter(Q(role="branch head")|Q(role='member'))
			return Response({
				"status":True, 
				"status_code" : HTTP_200_OK, 
				"users":UserListSerializer(users, many=True).data
				})
		return Response({
			"status":True, 
			"status_code" : HTTP_200_OK, 
			"message":"You Are Member User"
			})


class GetUser(APIView):

	def get(self, request, *args, **kwargs):

		user_id = kwargs.get("user_id")

		user = User.objects.filter(id=user_id).first()

		if user is not None:

			user_list = []
			user_dict = {}

			user_dict["id"] = user.id
			user_dict["first_name"] = user.first_name
			user_dict["middle_name"] = user.middle_name
			user_dict["last_name"] = user.last_name
			user_dict["email"] = user.email
			user_dict["phone"] = user.phone
			user_dict["aadhar"] = user.aadhar
			user_dict["country"] = user.country
			user_dict["state"] = user.state
			user_dict["city"] = user.city
			user_dict["constitucy"] = user.constitucy
			user_dict["ward"] = user.ward
			user_dict["landmark"] = user.landmark
			user_dict["pincode"] = user.pincode
			user_dict["gender"] = user.gender
			user_dict["date_of_birth"] = user.date_of_birth
			user_dict["role"] = user.role
			user_dict["occupation_type"] = user.occupation_type
			user_dict["occupation_title"] = user.occupation_title

			user_family = UserFamily.objects.filter(user=user.id).all()
			user_family_list = []

			for uf in user_family:
				user_family_dict = {}
				user_family_dict["name"] = uf.name
				user_family_dict["age"] = uf.age
				user_family_dict["aadhar"] = uf.aadhar
				user_family_dict["occupation_type"] = uf.occupation_type
				user_family_dict["occupation_title"] = uf.occupation_title
				user_family_list.append(user_family_dict)

			user_dict["user_family"] = user_family_list
			user_list.append(user_dict)

			return Response({"status":True, "status_code":HTTP_200_OK, "user": user_list})
		else:
			return Response({{"status":False, "status_code":HTTP_204_NO_CONTENT, "message":"User does not exists"}})


class Profile(APIView):

    def get(self, request):

    	user = User.objects.filter(id=request.user.id).first()

    	if user is not None:

    		user_list = []
    		user_dict = {}

    		user_dict["id"] = user.id
    		user_dict["first_name"] = user.first_name
    		user_dict["middle_name"] = user.middle_name
    		user_dict["last_name"] = user.last_name
    		user_dict["email"] = user.email
    		user_dict["phone"] = user.phone
    		user_dict["aadhar"] = user.aadhar
    		user_dict["country"] = user.country
    		user_dict["state"] = user.state
    		user_dict["city"] = user.city
    		user_dict["constitucy"] = user.constitucy
    		user_dict["ward"] = user.ward
    		user_dict["landmark"] = user.landmark
    		user_dict["pincode"] = user.pincode
    		user_dict["gender"] = user.gender
    		user_dict["date_of_birth"] = user.date_of_birth
    		user_dict["role"] = user.role
    		user_dict["occupation_type"] = user.occupation_type
    		user_dict["occupation_title"] = user.occupation_title

    		user_family = UserFamily.objects.filter(user=user.id).all()
    		user_family_list = []

    		for uf in user_family:
    			user_family_dict = {}
    			user_family_dict["id"] = uf.id
    			user_family_dict["name"] = uf.name
    			user_family_dict["age"] = uf.age
    			user_family_dict["aadhar"] = uf.aadhar
    			user_family_dict["occupation_type"] = uf.occupation_type
    			user_family_dict["occupation_title"] = uf.occupation_title
    			user_family_list.append(user_family_dict)

    		user_dict["user_family"] = user_family_list

    		user_list.append(user_dict)

    		return Response({"status":True, "status_code":HTTP_200_OK, "user": user_list})
    	else:
    		return Response({{"status":False, "status_code":HTTP_204_NO_CONTENT, "message":"User does not exists"}})


class EditUserProfile(APIView):

	@transaction.atomic
	def put(self, request):

		user_id = request.user.id
		user = User.objects.filter(id=user_id).first()

		if user is not None:

			user.first_name = request.data.get("first_name")
			user.middle_name = request.data.get("middle_name")
			user.last_name = request.data.get("last_name")
			user.country = request.data.get("country")
			user.state = request.data.get("state")
			user.city = request.data.get("city")
			user.constitucy = request.data.get("constitucy")
			user.ward = request.data.get("ward")
			user.landmark = request.data.get("landmark")
			user.pincode = request.data.get("pincode")
			user.gender = request.data.get("gender")
			user.date_of_birth = request.data.get("date_of_birth")
			user.occupation_type = request.data.get("occupation_type")
			user.occupation_title = request.data.get("occupation_title")
			user.save()
			return Response({"status": True, "status_code" : HTTP_200_OK, "message":"User Profile Updated."})
		else:
			return Response({"status":False, "status_code":HTTP_302_FOUND, "message":"User Does Not Exist."})


class DeleteUserFamilyMember(APIView):

	@transaction.atomic
	def delete(self, request, *args, **kwargs):

		family_member_id = kwargs.get("family_member_id")
		user_id = request.user.id

		user = User.objects.get(id=user_id)
		if user is not None:
			family_member = UserFamily.objects.filter(id=family_member_id, user=user.id).first()
			if family_member is not None:
				family_member.delete()
				return Response({"status":True, "status_code":HTTP_200_OK, "message":"Family Member Delete Successfully."})
			else:
				return Response({"status":True, "status_code":HTTP_302_FOUND, "message":"Family Member Does Not Exist."})
		else:
			return Response({"status":True, "status_code":HTTP_302_FOUND, "message":"User Does Not Exist."})


class GetUserFamilyDetails(APIView):

	def get(self, request, *args, **kwargs):

		familyMember_id = kwargs.get("id")
		user_id = request.user.id

		user = User.objects.filter(id=user_id).first()

		if user is not None:

			user_family_member = UserFamily.objects.filter(id=familyMember_id, user=user.id).first()
		
			return Response({"status": True, "status_code" : HTTP_200_OK, 
					"user family":UserFamilySerializer(user_family_member).data})
		else:
			return Response({"status":False, "status_code":HTTP_204_NO_CONTENT, "message":"User Does Not Exist."})

class EditUserFamilyMember(APIView):

	@transaction.atomic
	def put(self, request, *args, **kwargs):

		familyMember_id = kwargs.get("family_member_id")
		user_id = request.user.id

		user = User.objects.filter(id=user_id).first()
		if user is not None:

			user_family = UserFamily.objects.filter(id=familyMember_id, user=user.id).first()

			if user_family is not None:

				user_family.name = request.data.get("name")
				user_family.age = request.data.get("age")
				user_family.occupation_type = request.data.get("occupation_type")
				user_family.occupation_title = request.data.get("occupation_title")
				user_family.save()

				return Response({"status": True, "status_code" : HTTP_200_OK, "message":"User Family Member Updated."})
			else:
				return Response({"status":False, "status_code":HTTP_302_FOUND, "message":"User Family Member Does Not Exist."})
		else:
			return Response({"status":False, "status_code":HTTP_302_FOUND, "message":"User Does Not Exist."})
