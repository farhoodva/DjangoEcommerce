from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .forms import UserProfileEditForm
from .models import UserProfile, City
from core.models import Item
from RetailShopDjango.mixins import ProfileUpdateMixin


class UserProfileUpdateView(ProfileUpdateMixin, SuccessMessageMixin, generic.UpdateView):
    model = UserProfile
    form_class = UserProfileEditForm
    template_name = 'Profile.html'
    success_url = '/'
    success_message = 'You have updated your profile successfully'


class UserWishlistView(LoginRequiredMixin, generic.ListView):
    template_name = 'user_wishlist.html'
    context_object_name = 'items'

    def get_queryset(self):
        return Item.objects.all().filter(wishlist__username=self.request.user.username)


def load_cities(request):
    state_id = request.GET.get('state')
    cities = City.objects.filter(state_id=state_id)
    return render(request,'load_cities.html', {'cities': cities})