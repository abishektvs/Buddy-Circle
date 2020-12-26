from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from .models import Profile
from bootstrap4.widgets import RadioSelectButtonGroup
User = get_user_model()

class userCreateForm(UserCreationForm):

    def clean(self):
       email = self.cleaned_data.get('email')
       username = self.cleaned_data.get('username')
       if len(username) < 8:
            raise ValidationError("Username should contain atleast 8 characters")
       if User.objects.filter(email=email).exists():
            raise ValidationError("The Email you have entered already exists")
       return self.cleaned_data

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class UserProfileform(forms.ModelForm):
    username = forms.CharField(max_length=15, min_length=8)
    firstname = forms.CharField(max_length=15, required=True)
    lastname = forms.CharField(max_length=15, required=False)

    class Meta:
        model = Profile
        # exclude = ('user',)
        # for ordering fields
        fields = [ 'username',
                    'firstname',
                    'lastname',
                    'bio',
                    'dob',
                    'gender',
                    'profile_pic',
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'cols': 80, 'rows': 2}),
            'dob': forms.DateInput(format =( r'%d/%m/%Y'),
                                    attrs={'type':'date'}
                    ),
            'gender' : forms.RadioSelect()
        }
        labels = {
            'dob': _('Date of Birth'),
        }
