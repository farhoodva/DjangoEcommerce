from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.urls import reverse


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=255, null=True, blank=True)
    lastname = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    profile_pic = models.ImageField(blank=True, null=True, upload_to='img/profile_pics')

    def __str__(self):
        return self.user.username

    def get_profile_update_url(self):

        return reverse('profile_update', kwargs={
            'pk': str(self.user_id)
        })


# django signals => Profile creation
def profile_creation_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(pk=instance.id, user=instance)


post_save.connect(profile_creation_signal, sender=User)
