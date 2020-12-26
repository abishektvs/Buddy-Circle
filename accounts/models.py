from django.db import models
from django.contrib import auth
from django.utils import timezone
from datetime import datetime, date
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(auth.models.User, auth.models.PermissionsMixin):
    friends = models.ManyToManyField('self', blank=True, through="friends", symmetrical=False)

    def __str__(self):
        return f'@{self.username}'

class Profile(models.Model):
    GENDERS = (
            ('M', 'Male'),
            ('F', 'Female'),
        )
    user = models.OneToOneField(auth.get_user_model(), null=True, on_delete=models.CASCADE)
    bio = models.TextField(null=True, default='')
    profile_pic = models.ImageField(null=True, default='')
    gender = models.CharField(max_length=1, choices=GENDERS, null=True, default='')
    dob = models.DateField(null=True, blank=False)
    age = models.PositiveIntegerField(null = True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.dob != None:
            today = timezone.now()
            self.age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        super().save(*args, **kwargs)

@receiver(post_save, sender=auth.get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# @receiver(post_save, sender=auth.get_user_model())
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

class Friends(models.Model):
    REQUEST_STATUS_CHOICES = [
        ( 'NR', 'No request'),
        ( 'SENT', 'Request Sent'),
        ( 'DONE', 'Accepted Request')
    ]
    user_requested = models.ForeignKey(auth.get_user_model(), related_name="user_ref", on_delete=models.CASCADE)
    friend = models.ForeignKey(auth.get_user_model(), related_name="user_friend", on_delete=models.CASCADE)
    request_status = models.CharField(max_length=30, default='NR', choices=REQUEST_STATUS_CHOICES,)
    hand_shaked_on = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.user_requested.username} {self.request_status} {self.friend.username}'

    def save(self, *args, **kwargs):
        if self.request_status == "DONE":
            self.hand_shaked_on = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ("user_requested", "friend")