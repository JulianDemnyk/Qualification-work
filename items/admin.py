from django.contrib import admin

from .models import *

admin.site.register(Motherboard_model)
admin.site.register(Cpu_model)
admin.site.register(Gpu_model)
admin.site.register(Ram_model)
admin.site.register(Storage_model)
admin.site.register(Case_model)
admin.site.register(Cooling_system_model)
admin.site.register(Power_supply_model)
admin.site.register(Computer_build)

