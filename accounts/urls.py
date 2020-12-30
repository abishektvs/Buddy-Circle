from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', views.Login.as_view(template_name='accounts/login.html'), name='login'),
    path('all-users/in-buddycircle', views.AllUserView.as_view(), name='allusers'),
    path('profile-details/for/<pk>/', views.UserProfileView.as_view(), name='userprofile'),
    path('edit-profile-details/for/<pk>/', views.EditUserProfile.as_view(), name='edit_userprofile'),
    path('follow-requests/for/<slug:username>/', views.FollowRequests.as_view(), name='follow_requests'),
    path('followed/by/<slug:username>/', views.FollowingList.as_view(), name='following_list'),
    path('<slug:username>/following/', views.FollowersList.as_view(), name='followers_list'),
    path('send-request/to/<slug:follower_username>/', 
        views.SendFollowRequest.as_view(), name='send_follow_request'
    ),
    path('accept-follow-request/from/<slug:follower_username>/', 
        views.AcceptFollowRequest.as_view(), name='accept_request'
    ),
    path('remove/<slug:follower_username>/', views.UnFollowUser.as_view(), name='unfollow'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]