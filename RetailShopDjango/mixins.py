from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

from users.models import UserProfile


class ProfileUpdateMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        profile = UserProfile.objects.get(pk=kwargs['pk'])
        if not request.user.id == profile.user.id:
            messages.warning(request, "You don't have permission")
            return redirect('core:home')
        return super().dispatch(request, *args, **kwargs)

