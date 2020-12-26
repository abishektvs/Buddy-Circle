from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse

class index(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("homefeed", kwargs={'username':self.request.user.username}))
        return super().get(request, *args, **kwargs)

class UserHome(TemplateView):
    template_name = "user_homepage.html"

class exitpage(TemplateView):
    template_name = "exitpage.html"
