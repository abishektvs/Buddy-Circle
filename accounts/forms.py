from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from bootstrap4.widgets import RadioSelectButtonGroup
from .models import Profile

User = get_user_model()

class userCreateForm(UserCreationForm):
    gender = forms.ChoiceField(
        choices=(
            ('M', _('Male')),
            ('F', _('Female'))
        ), 
        widget=forms.RadioSelect
    )

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
        fields = ('username', 'first_name', 'last_name', 'gender', 'email', 'password1', 'password2')


class UserProfileform(forms.ModelForm):
    class Meta:
        model = Profile
        # exclude = ('user',)
        # but for ordering fields if missed ordering in models
        fields = ['bio', 'dob', 'gender', 'profile_pic']
        widgets = {
            'bio': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
            'dob': forms.DateInput(
                        format =( r'%d/%m/%Y'),
                        attrs={'type':'date','value':'23-03-1999'}
                    ),
            'gender': forms.RadioSelect()
        }
        labels = {
            'dob': _('Date of Birth'),
        }
