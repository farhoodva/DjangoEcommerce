from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.urls import reverse


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=255, null=True, blank=True)
    lastname = models.CharField(max_length=255, null=True, blank=True)
    address_line = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True,blank=True)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    state = models.ForeignKey('State', on_delete=models.SET_NULL, null=True, blank=True, )
    city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True, blank=True)
    profile_pic = models.ImageField(blank=True, null=True, upload_to='img/profile_pics')

    class Meta:
        verbose_name_plural = 'Shipping info'

    def __str__(self):
        return self.user.username

    def get_profile_update_url(self):
        return reverse('profile_update', kwargs={
            'pk': str(self.user_id)
        })

    def get_billing_url(self):
        return reverse('core:checkout', kwargs={
            'pk': str(self.user_id)
        })


class State(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=50)
    state = models.ForeignKey('State', on_delete=models.CASCADE)

    class Meta:
        ordering = ['state']
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name


# django signals => Profile creation
def profile_creation_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            pk=instance.id,
            user=instance,
            firstname=instance.first_name,
            lastname=instance.last_name,
        )


post_save.connect(profile_creation_signal, sender=User)
