"""swiper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from user import apis as user_api

urlpatterns = [
    path('api/user/submit/phone/', user_api.submit_phone),
    path('api/user/submit/vcode/', user_api.submit_vcode),
    path('api/user/get/profile/', user_api.get_profile),
    path('api/user/edit/profile/', user_api.edit_profile),
    path('api/user/upload/avatar/', user_api.upload_avatar),

]
