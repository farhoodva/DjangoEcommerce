from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .forms import UserProfileEditForm
from .models import UserProfile
from RetailShopDjango.mixins import ProfileUpdateMixin


class UserProfileUpdateView(ProfileUpdateMixin, SuccessMessageMixin, generic.UpdateView):
    model = UserProfile
    form_class = UserProfileEditForm
    template_name = 'Profile.html'
    success_url = '/'
    success_message = 'You have updated your profile successfully'
