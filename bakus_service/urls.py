"""bakus_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from knox import views as knox_views

from addition import external_views, views

urlpatterns = [
    path("admin/", admin.site.urls),
    # API v1
    path("api/v1/addition/", views.AdditionListView.as_view(), name="addition-list"),
    path("api/v1/addition/<uuid:id>/", views.AdditionDetailView.as_view(), name="addition-detail"),
    path(
        "api/v1/addition/<uuid:id>/rename-movie", views.AdditionRenameMovieView.as_view(), name="addition-rename-movie"
    ),
    path(
        "api/v1/addition/<uuid:id>/rename-tv-season",
        views.AdditionRenameTvSeasonView.as_view(),
        name="addition-rename-tv-season",
    ),
    path("api/v1/auth/account/", views.AccountView.as_view(), name="account-detail"),
    path("api/v1/auth/login/", views.LoginView.as_view(), name="knox_login"),
    path("api/v1/auth/logout/", knox_views.LogoutView.as_view(), name="knox_logout"),
    path("api/v1/auth/logoutall/", knox_views.LogoutAllView.as_view(), name="knox_logoutall"),
    # External requirements
    path(
        ".well-known/apple-app-site-association",
        external_views.AppleAppSiteAssociationView.as_view(),
        name="apple-app-site-association",
    ),
]
