from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.views.generic import TemplateView

from .views import HomePage, activity, response


urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("account/social/accounts/", TemplateView.as_view(template_name="account/social.html"), name="account_social_accounts"),
    path("account/social/", include("social_django.urls", namespace="social")),

    path("activity/", activity, name="activity"),
    path("response/<int:pk>/", response, name="response")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
