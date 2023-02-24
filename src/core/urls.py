from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularSwaggerView


v1_api_urls = [
    path("users/", include("users.urls")),
]

api_urls = [
    path("v1/", include((v1_api_urls, "v1"), namespace="v1")),
]

docs_urls = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]

admin_urls = [
    path("jet/", include("jet.urls", "jet")),
    path("jet/dashboard/", include("jet.dashboard.urls", "jet-dashboard")),
    path("admin/", admin.site.urls),
]

urlpatterns = [
    path("api/", include((api_urls, "api"), namespace="api")),
    path("", include(docs_urls)),
    path("", include(admin_urls)),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]

# TODO: Another boolean to turn on and off silk
if settings.DEBUG:
    urlpatterns += [
        path("silk/", include("silk.urls", namespace="silk")),
    ]
