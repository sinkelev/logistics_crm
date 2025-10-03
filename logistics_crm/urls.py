"""
URL configuration for logistics_crm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from logistics.api import RouteViewSet
from warehouse.api import OrderViewSet
from finance.api import ExpenseViewSet

router = DefaultRouter()
router.register(r"routes", RouteViewSet)
router.register(r"cargoes", OrderViewSet)
router.register(r"expenses", ExpenseViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls)),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="frontend/login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("", include("frontend.urls")),
    path("", include("accounts.urls")),
]
