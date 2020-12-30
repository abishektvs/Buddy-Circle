from django.db import models
from django.contrib import auth
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, date
import uuid

class User(auth.models.User, auth.models.PermissionsMixin):
    user_uuid = uuid.uuid4()
    buddies = models.ManyToManyField('self', blank=True, through="Buddy", symmetrical=False)

    def __str__(self):
        return f'@{self.username}'

class Profile(models.Model):
    GENDERS = (
            ('M', 'Male'),
            ('F', 'Female'),
        )
    user = models.OneToOneField(auth.get_user_model(), null=True, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank='', default='')
    profile_pic = models.ImageField(upload_to='profilepics/', null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDERS, null=True, blank=False)
    dob = models.DateField(null=True, blank=False) 
    age = models.PositiveIntegerField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.dob != None:
            today = timezone.now()
            self.age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))

        if self.profile_pic == '':
            print('inside propic')
            if self.gender == 'M':
                self.profile_pic = 'profilepics/maledefault.jpg'
            elif self.gender == 'F':
                self.profile_pic = 'profilepics/femaledefault.jpg'
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username + "'s profile" 

@receiver(post_save, sender=auth.get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class Buddy(models.Model):
    REQUEST_STATUS_CHOICES = [
        ( 'SENT', 'Request Sent'),
        ( 'DONE', 'Accepted Request'),
        ( 'BLOCK', 'blocked')
    ]
    requested_from = models.ForeignKey(auth.get_user_model(), related_name="requested_from", on_delete=models.CASCADE)
    requested_to = models.ForeignKey(auth.get_user_model(), related_name="requested_to", on_delete=models.CASCADE)
    request_status = models.CharField(max_length=30, blank=True, choices=REQUEST_STATUS_CHOICES,)
    hand_shaked_on = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.request_status == "DONE":
            self.hand_shaked_on = timezone.now()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.requested_from.username} {self.request_status} {self.requested_to.username}'

    class Meta:
        unique_together = ("requested_from", "requested_to") 