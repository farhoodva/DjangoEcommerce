from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import redirect
from django.conf import settings


class MyAccountAdapter(DefaultAccountAdapter):

    # def get_login_redirect_url(self, request):
    #     return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    def get_login_redirect_url(self, request):
        path = request.get_full_path()
        print(path)
        return path
