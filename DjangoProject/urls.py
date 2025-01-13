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
        fetch_all_rams

urlpatterns = [
        path('admin/', admin.site.urls),
        path('compatibility/', compatibility_page, name='compatibility_page'),
        path('get_compatible_components/', get_compatible_components, name='get_compatible_components'),
        path('fetch-all-cpus/', fetch_all_cpus, name='fetch_all_cpus'),
        path('fetch-all-motherboards/', fetch_all_motherboards, name='fetch_all_motherboards'),
        path('fetch-all-rams/', fetch_all_rams, name='fetch_all_rams'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)