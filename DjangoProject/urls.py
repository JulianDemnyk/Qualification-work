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
from items.views import compatibility_page, get_compatible_components, fetch_all_cpus, fetch_all_motherboards, \
        fetch_all_rams, fetch_all_cooling_systems, fetch_all_gpus, fetch_all_power_supplies, fetch_all_cases, \
        fetch_all_storages, save_computer_build, detail_view_cpu, home_view, detail_view_motherboard, detail_view_gpu, \
        detail_view_ram, detail_view_storage, detail_view_cooling_system, detail_view_power_supply, detail_view_case, \
        list_view_cpu

urlpatterns = [
        path('admin/', admin.site.urls),
        path('', home_view, name='home'),
        path('compatibility/', compatibility_page, name='compatibility_page'),
        path('save_build/', save_computer_build, name='save_computer_build'),
        path('get_compatible_components/', get_compatible_components, name='get_compatible_components'),
        path('fetch_all_cpus/', fetch_all_cpus, name='fetch_all_cpus'),
        path('fetch_all_motherboards/', fetch_all_motherboards, name='fetch_all_motherboards'),
        path('fetch_all_rams/', fetch_all_rams, name='fetch_all_rams'),
        path('fetch_all_cooling_systems', fetch_all_cooling_systems, name='fetch_all_cooling_systems'),
        path('fetch_all_gpus', fetch_all_gpus, name='fetch_all_gpus'),
        path('fetch_all_power_supplies/', fetch_all_power_supplies, name='fetch_all_power_supplies'),
        path('fetch_all_cases/', fetch_all_cases, name='fetch_all_cases'),
        path('fetch_all_storages/', fetch_all_storages, name='fetch_all_storages'),
        path('cpu_detail/<int:id>/', detail_view_cpu, name='detail_view_cpu'),
        path('cpu_detail/', list_view_cpu, name='list_view_cpu'),
        path('motherboard_detail/<int:id>/', detail_view_motherboard, name='detail_view_motherboard'),
        path('gpu_detail/<int:id>/', detail_view_gpu, name='detail_view_gpu'),
        path('ram_detail/<int:id>/', detail_view_ram, name='detail_view_ram'),
        path('storage_detail/<int:id>/', detail_view_storage, name='detail_view_storage'),
        path('cooling_system_detail/<int:id>/', detail_view_cooling_system, name='detail_view_cooling_system'),
        path('power_supply_detail/<int:id>/', detail_view_power_supply, name='detail_view_cooling_system'),
        path('case_detail/<int:id>/', detail_view_case, name='detail_view_case'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)