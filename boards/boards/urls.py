"""
URL configuration for boards project.

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
from notices import views as notices_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', notices_views.home, name='home'),
    path('home.html', notices_views.home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('register/', notices_views.register, name='register'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('create_board.html', notices_views.create_board, name='create_board'),
    path('view_board/<int:pk>/', notices_views.view_board, name='view_board'),
    path('view_board/<int:pk>/create_notice.html', notices_views.create_notice, name='create_notice')
]