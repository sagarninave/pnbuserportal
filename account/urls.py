from django.urls import path
from .views import (RegisterUser, Users, SendOTP, Login, Logout, Profile, AddUserFamily, GetUser, EditUserProfile,
GetUserFamilyDetails, EditUserFamilyMember, DeleteUserFamilyMember)

urlpatterns = [
    path('users', Users.as_view(), name="users"),
    path('getuser/<str:user_id>', GetUser.as_view(), name="getuser"),
    path('register', RegisterUser.as_view(), name="register_user"),
    path('send-otp', SendOTP.as_view(), name="send-otp"),
    path('login', Login.as_view(), name="login"),
    path('logout', Logout.as_view(), name="logout"),
    path('profile', Profile.as_view(), name="profile"),
    path('addfamilymember', AddUserFamily.as_view(), name="addfamilymember"),
    path('edituserprofile', EditUserProfile.as_view(), name="edituserprofile"),
    path('getuserfamilydetails/<str:id>', GetUserFamilyDetails.as_view(), name="getuserfamilydetails"),
    path('edituserfamilymember/<str:family_member_id>', EditUserFamilyMember.as_view(), name="edituserfamilymember"),
    path('deleteuserfamilymember/<str:family_member_id>', DeleteUserFamilyMember.as_view(), name="deleteuserfamilymember"),
]