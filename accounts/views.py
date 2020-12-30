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

from . import forms
from .models import Buddy,Profile

User = get_user_model()

class Login(LoginView):

    def get_success_url(self):
        return reverse('homefeed',kwargs={'username':self.request.user.username})

class SignUp(CreateView):
    form_class = forms.userCreateForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        self.object = form.save()
        signup_user_profile = get_object_or_404(Profile, user=self.object)
        signup_user_profile.gender = form["gender"].value()
        signup_user_profile.save()
        return super().form_valid(form)

class AllUserView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'accounts/all_user_list.html'
    context_object_name = 'useraccounts'
    def get_queryset(self): 
        return User.objects.select_related('profile').order_by('username')

class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/userdetails.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        requested_user = context['user']
        following = Buddy.objects.filter(requested_from=requested_user,request_status='DONE').count()
        followers = Buddy.objects.filter(requested_to=requested_user,request_status='DONE').count()
        context["followers_count"] = followers
        context["following_count"] = following
        print(context['user'])
        print(context)
        return context

class EditUserProfile(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'accounts/edit_userdetails.html'
    form_class = forms.UserProfileform

    def get(self, request, *args, **kwargs):
        if int(self.kwargs.get('pk')) != self.request.user.profile.id:
            return HttpResponseRedirect(reverse("accounts:userprofile",kwargs={"pk": self.request.user.id}))
        else:
            return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        requested_user = form.save(commit=False)
        form_input = self.request.POST
        requested_user.user.username = form_input['username']
        requested_user.user.first_name = form_input['firstname']
        requested_user.user.last_name = form_input['lastname']
        requested_user.user.save()
        return super().form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse("accounts:userprofile", kwargs={'pk':self.request.user.id})

class FollowRequests(LoginRequiredMixin, ListView):
    model = Buddy
    template_name = 'accounts/follow_request_list.html'
    context_object_name = 'follow_requests'

    def get_queryset(self):
        this_user = User.objects.filter(username=self.kwargs.get("username")).get()
        self.follow_requests = Buddy.objects.filter(
                                    requested_to = this_user,
                                    request_status = 'SENT'
                                ).all()
        print(self.follow_requests)
        return self.follow_requests

class FollowersList(LoginRequiredMixin, ListView):
    model = Buddy
    template_name = 'accounts/followers_list.html'
    context_object_name = 'followers_list'

    def get_queryset(self):
        this_user = User.objects.filter(username=self.kwargs.get("username")).get()
        print(this_user)
        followers_list = Buddy.objects.filter(
                            requested_to=this_user,
                            request_status='DONE',
                        ).prefetch_related('requested_from','requested_to').all()
        return(followers_list)
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context

class FollowingList(LoginRequiredMixin, ListView):
    template_name = 'accounts/following_list.html'
    model = Buddy
    context_object_name = 'following_list'

    def get_queryset(self):
        print(self.kwargs.get("username"))
        this_user = User.objects.filter(username=self.kwargs.get("username")).get()
        print(this_user)

        following_list = Buddy.objects.filter(
                            requested_from = this_user,
                            request_status = 'DONE',
                        ).prefetch_related('requested_from','requested_to').all()
        return(following_list)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context

class SendFollowRequest(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("accounts:allusers")

    def get(self,  request, *args, **kwargs):
        requested_from = self.request.user
        print(self.kwargs.get("follower_username"))
        requested_to = get_object_or_404(User,username=self.kwargs.get("follower_username"))

        if requested_from.id != requested_to.id:
            try:
                Buddy.objects.create(
                    requested_from=requested_from,
                    requested_to=requested_to,
                    request_status='SENT'
                )
            except IntegrityError:
                messages.warning(self.request,
                    ("Warning, already sent follow request to {}".format(requested_to.username))
                )
            else:
                messages.success(self.request,"Request sent to {}.".format(requested_to.username))

        return super().get(request, *args, **kwargs)

class AcceptFollowRequest(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("accounts:follow_requests", kwargs={'username':self.request.user.username})
    
    def get(self, request, *args, **kwargs):
        follower = get_object_or_404(User, username=self.kwargs.get("follower_username"))
        accept_buddy = Buddy.objects.get(
                            requested_from=follower, 
                            requested_to=self.request.user,
                        )
        print(accept_buddy)
        accept_buddy.request_status = "DONE"
        accept_buddy.save()
        return super().get(request, *args, **kwargs)

class UnFollowUser(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("accounts:allusers")

    def get(self, request, *args, **kwargs):
        user = User.objects.filter(username=self.kwargs.get("friendname")).get()
        try:
            buddy = Buddy.objects.filter(
                requested_from=self.request.user,
                requested_to=user
            ).get()

        except Buddy.DoesNotExist:
            messages.warning(
                self.request,
                "You both haven't shaked hands"
            )

        else:
            buddy.delete()
            messages.success(
                self.request,
                "You have successfully unfriended."
            )