from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from users.views import UserProfileUpdateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls',namespace='core')),
    path('accounts/', include('allauth.urls')),
    path('Profile/<int:pk>', UserProfileUpdateView.as_view(), name='profile_update'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
