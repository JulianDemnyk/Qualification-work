"""
URL configuration for DjangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from items import views
from items.views import user_profile

urlpatterns = [
        path('admin/', admin.site.urls),
        path('', views.home_view, name='home'),
        path('profile', user_profile, name='profile'),
        path('compatibility/', views.compatibility_page, name='compatibility_page'),
        path('save_computer_build/', views.save_computer_build, name='save_computer_build'),
        path('get_compatible_components/', views.get_compatible_components, name='get_compatible_components'),
        path('builds/<int:id>/', views.detail_view_build, name='detail_view_build'),
        path('cpus/<int:id>/', views.detail_view_cpu, name='detail_view_cpu'),
        path('cpus/', views.list_view_cpu, name='list_view_cpu'),
        path('motherboards/<int:id>/', views.detail_view_motherboard, name='detail_view_motherboard'),
        path('motherboards/', views.list_view_motherboard, name='list_view_motherboard'),
        path('gpus/<int:id>/', views.detail_view_gpu, name='detail_view_gpu'),
        path('gpus/', views.list_view_gpu, name='list_view_gpu'),
        path('rams/<int:id>/', views.detail_view_ram, name='detail_view_ram'),
        path('rams/', views.list_view_ram, name='list_view_ram'),
        path('storages/<int:id>/', views.detail_view_storage, name='detail_view_storage'),
        path('storages/', views.list_view_storage, name='list_view_storage'),
        path('cooling_systems/<int:id>/', views.detail_view_cooling_system, name='detail_view_cooling_system'),
        path('cooling_systems/', views.list_view_cooling_system, name='list_view_cooling_system'),
        path('power_supplys/<int:id>/', views.detail_view_power_supply, name='detail_view_power_supply'),
        path('power_supplys/', views.list_view_power_supply, name='list_view_power_supply'),
        path('cases/<int:id>/', views.detail_view_case, name='detail_view_case'),
        path('cases/', views.list_view_case, name='list_view_case'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)