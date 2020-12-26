from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', views.MyLoginView.as_view(template_name='accounts/login.html'),name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('addfriend/<slug:friendname>/', views.SendFriendRequest.as_view(), name='friendreq'),
    path('friend-requests/for/<slug:username>', views.FriendRequestsList.as_view(), name='friend_request_list'),
    path('<slug:user_name>/friend-list/', views.FriendListView.as_view(), name='friendlist'),
    path('friendrequest/to/<slug:friendname>/', views.AcceptFriendRequest.as_view(), name='addfriend'),
    path('remove-friend/<slug:friendname>/', views.RemoveFriend.as_view(), name='removefriend'),
    path('account-details/for/<pk>/', views.UserProfileView.as_view(), name='userprofile'),
    path('all-users/in-buddycircle', views.AllUserView.as_view(), name='allusers'),
    path('edit-details/for/<pk>/', views.EditUserProfile.as_view(), name='edituserdetails')
]