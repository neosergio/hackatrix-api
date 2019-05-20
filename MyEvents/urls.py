"""MyEvents URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import include
from django.urls import path
from rest_framework_swagger.views import get_swagger_view


schema_view = get_swagger_view(title='Hackatrix API')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('assessments/', include('assessments.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('events/', include('events.urls')),
    path('ideas/', include('ideas.urls')),
    path('swagger/', schema_view),
    path('users/', include('users.urls')),
]
