from django.views.generic import (
    CreateView, 
    RedirectView, 
    ListView, 
    DetailView,
    UpdateView
)
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import get_user_model
User = get_user_model()

from .models import Friends,Profile
from .models import User as UserProfile
from . import forms

class MyLoginView(LoginView):

    def get_success_url(self):
        return reverse('homefeed',kwargs={'username':self.request.user.username})

class SignUp(CreateView):
    form_class = forms.userCreateForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')

class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/userdetails.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        requested_user = context['user']
        following = Friends.objects.filter(user_requested=requested_user,request_status='DONE').count()
        followers = Friends.objects.filter(friend=requested_user,request_status='DONE').count()
        context["followers_count"] = followers
        context["following_count"] = following
        print(context['user'])
        print(context)
        return context

class EditUserProfile(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'accounts/edit_userdetails.html'
    form_class =  forms.UserProfileform

    def get(self, request, *args, **kwargs):
        if int(self.kwargs.get('pk')) != self.request.user.profile.id:
            return HttpResponseRedirect(reverse("accounts:userprofile",kwargs={"pk": self.request.user.id}))
        else:
            return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        requested_user = get_object_or_404(User,id=self.request.user.id)
        requested_user.username = form["username"].value()
        requested_user.first_name = form["firstname"].value()
        requested_user.last_name = form["lastname"].value()
        requested_user.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context

    def get_success_url(self, *args, **kwargs):
        return reverse("accounts:userprofile", kwargs={'pk':self.request.user.id})
    
class AllUserView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'accounts/all_user_list.html'
    context_object_name = 'useraccounts'
    def get_queryset(self): 
        return User.objects.select_related('profile').order_by('username')

class FriendRequestsList(LoginRequiredMixin, ListView):
    model = Friends
    template_name = 'accounts/friend_request_list.html'
    context_object_name = 'friend_requests'

    def get_queryset(self):
        try:
            self.users_friends = Friends.objects.filter(
                friend=self.request.user,
                request_status = 'SENT'
            ).all()
            print(self.users_friends)
            return self.users_friends
        except User.DoesNotExist:
            raise 'error'

class SendFriendRequest(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("accounts:allusers")

    def get(self,  request, *args, **kwargs):
        friend = get_object_or_404(User,username=self.kwargs.get("friendname"))
        user_requested = self.request.user
        if user_requested.id != friend.id:
            try:
                Friends.objects.create(user_requested=user_requested,friend=friend,request_status='SENT')

            except IntegrityError:
                messages.warning(self.request,("Warning, already a friend {}".format(friend.username)))

            else:
                messages.success(self.request,"Request sent to {}.".format(friend.username))

        return super().get(request, *args, **kwargs)

class FriendListView(LoginRequiredMixin, ListView):
    template_name = 'accounts/friend_list.html'
    model = Friends

    def get_queryset(self):
        try:
            self.users_friends = User.objects.prefetch_related('user_friend','user_ref').get(
                id = self.request.user.id
            )
            print(self.users_friends)
            return self.users_friends.user_ref.filter(request_status = 'DONE')
        except User.DoesNotExist:
            raise 'error'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context

class RemoveFriend(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("accounts:friendlist",kwargs={"user_name": self.request.user.username})
    
    def get(self, request, *args, **kwargs):
        friend = User.objects.filter(username=self.kwargs.get("friendname")).get()
        try:
            friend = Friends.objects.filter(
                user_requested=self.request.user,
                friend=friend
            ).get()

        except Friends.DoesNotExist:
            messages.warning(
                self.request,
                "You both haven't shaked hands"
            )

        else:
            friend.delete()
            messages.success(
                self.request,
                "You have successfully unfriended."
            )
        return super().get(request, *args, **kwargs)

class AcceptFriendRequest(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("accounts:allusers")
    
    def get(self, request, *args, **kwargs):
        friend = get_object_or_404(User, username=self.kwargs.get("friendname"))
        accept = Friends.objects.get(user_requested=friend,friend=self.request.user)
        print(accept)
        accept.request_status = "DONE"
        accept.save()

        return super().get(request, *args, **kwargs)

