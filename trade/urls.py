from django.urls import path
from .views import HomeView

from .views import simulation

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", HomeView.as_view(), name='home'),
    path("api/v1/simple", simulation, name='simulate_simple'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
