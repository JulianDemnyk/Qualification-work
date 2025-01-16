from django.contrib import admin

from .models import Motherboard_model, Cpu_model, Gpu_model, Ram_model, Storage_model, Case_model, Cooling_system_model, \
    Computer_build, Power_supply_model

# Register your models here.

admin.site.register(Motherboard_model)
admin.site.register(Cpu_model)
admin.site.register(Gpu_model)
admin.site.register(Ram_model)
admin.site.register(Storage_model)
admin.site.register(Case_model)
admin.site.register(Cooling_system_model)
admin.site.register(Power_supply_model)
admin.site.register(Computer_build)