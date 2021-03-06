from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from .settings import DEBUG
from .view import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls'), name="records"),
    path('api/markers/', include('map.urls')),
    path('api/market/', include('market.urls')),
    re_path(r'^$', home_view),
    re_path(r'^(!admin\/)(!api\/\w+)\w+', home_view)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
