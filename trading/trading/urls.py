from django.contrib import admin
from django.conf import settings
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('authentication.urls')),
    path('', include('offer.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('debug/', include(debug_toolbar.urls)),
    ] + urlpatterns
