"""
URL configuration for ems project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework import routers
from forms_app.views import FormTemplateViewSet, FormFieldViewSet
from employees.views import EmployeeViewSet
from accounts.views import RegisterView, ProfileView, ChangePasswordView, AdminUserListView, AdminUserDetailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import home, auth_page
from .views import profile_page

router = routers.DefaultRouter()
router.register(r"forms", FormTemplateViewSet, basename="formtemplate")
router.register(r"fields", FormFieldViewSet, basename="formfield")
router.register(r"employees", EmployeeViewSet, basename="employee")

urlpatterns = [
    path("", home, name="home"),
    path("auth/", auth_page, name="auth_page"),
    path('admin/', admin.site.urls),
    path("api/", include(router.urls)),
    path("api/auth/register/", RegisterView.as_view(), name="register"),
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/profile/", ProfileView.as_view(), name="profile"),
    path("api/admin/users/", AdminUserListView.as_view(), name="admin_user_list"),
    path("profile/", profile_page, name="profile_page"),
    path("api/admin/users/<int:pk>/", AdminUserDetailView.as_view(), name="admin_user_detail"),
    path("api/auth/change-password/", ChangePasswordView.as_view(), name="change_password"),
]
