from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Motherboard_model(models.Model):
    motherboard_name = models.TextField(max_length=100)
    motherboard_manufacturer = models.TextField(max_length=100)
    motherboard_socket = models.TextField(max_length=10)
    motherboard_chipset = models.TextField(max_length=10)
    motherboard_ram_type = models.TextField(max_length=10)
    motherboard_ram_slot = models.IntegerField()
    motherboard_pci_slot = models.IntegerField()
    motherboard_sata_slot = models.IntegerField()
    motherboard_m2_slot = models.IntegerField()
    motherboard_form_factor = models.CharField(max_length=10)
    motherboard_price = models.IntegerField()
    motherboard_description = models.TextField(max_length=1500, blank=True)
    motherboard_featured = models.BooleanField(default=True)
    motherboard_image = models.ImageField(default='fallback.png', blank=True)

    def __str__(self):
        return self.motherboard_name

class Cpu_model(models.Model):
    cpu_name = models.TextField(max_length=100)
    cpu_manufacturer = models.TextField(max_length=100)
    cpu_type = models.TextField(max_length=100)
    cpu_socket = models.TextField(max_length=10)
    cpu_cores = models.IntegerField()
    cpu_threads = models.IntegerField()
    cpu_clock_speed = models.TextField(max_length=10)
    cpu_tdp = models.IntegerField()
    cpu_power_consumption = models.IntegerField()
    cpu_price = models.IntegerField()
    cpu_description = models.TextField(max_length=1500, blank=True)
    cpu_featured = models.BooleanField(default=True)
    cpu_image = models.ImageField(default='fallback.png', blank=True)

    def __str__(self):
        return self.cpu_name

class Gpu_model(models.Model):
    gpu_name = models.TextField(max_length=100)
    gpu_manufacturer = models.TextField(max_length=100)
    gpu_chip = models.TextField(max_length=100)
    gpu_clock_speed = models.TextField(max_length=10)
    gpu_bits = models.IntegerField()
    gpu_ram = models.TextField(max_length=10)
    gpu_ram_type = models.TextField(max_length=10)
    gpu_power_consumption = models.IntegerField()
    gpu_price = models.IntegerField()
    gpu_description = models.TextField(max_length=1500, blank=True)
    gpu_featured = models.BooleanField(default=True)
    gpu_image = models.ImageField(default='fallback.png', blank=True)

    def __str__(self):
        return self.gpu_name

class Ram_model(models.Model):
    ram_name = models.TextField(max_length=100)
    ram_manufacturer = models.TextField(max_length=100)
    ram_type = models.TextField(max_length=10)
    ram_clock_speed = models.TextField(max_length=10)
    ram_size = models.TextField(max_length=10)
    ram_amount = models.IntegerField()
    ram_price = models.IntegerField()
    ram_description = models.TextField(max_length=1500, blank=True)
    ram_featured = models.BooleanField(default=True)
    ram_image = models.ImageField(default='fallback.png', blank=True)

    def __str__(self):
        return self.ram_name

class Storage_model(models.Model):
    storage_name = models.TextField(max_length=100)
    storage_manufacturer = models.TextField(max_length=100)
    storage_type = models.TextField(max_length=10)
    storage_capacity = models.TextField(max_length=10)
    storage_speed = models.TextField(max_length=10)
    storage_connection = models.TextField(max_length=10)
    storage_price = models.IntegerField()
    storage_description = models.TextField(max_length=1500, blank=True)
    storage_featured = models.BooleanField(default=True)
    storage_image = models.ImageField(default='fallback.png', blank=True)

    def __str__(self):
        return self.storage_name

class Cooling_system_model(models.Model):
    cooling_system_name = models.TextField(max_length=100)
    cooling_system_manufacturer = models.TextField(max_length=100)
    cooling_system_socket = models.TextField(max_length=100)
    cooling_system_tdp = models.IntegerField()
    cooling_system_type = models.CharField(max_length=10)
    cooling_system_price = models.IntegerField()
    cooling_system_description = models.TextField(max_length=1500, blank=True)
    cooling_system_featured = models.BooleanField(default=True)
    cooling_system_image = models.ImageField(default='fallback.png', blank=True)

    def __str__(self):
        return self.cooling_system_name

class Power_supply_model(models.Model):
    power_supply_name = models.TextField(max_length=100)
    power_supply_manufacturer = models.TextField(max_length=100)
    power_supply_power = models.IntegerField()
    power_supply_form_factor = models.CharField(max_length=10)
    power_supply_price = models.IntegerField()
    power_supply_description = models.TextField(max_length=1500, blank=True)
    power_supply_featured = models.BooleanField(default=True)
    power_supply_image = models.ImageField(default='fallback.png', blank=True)

    def __str__(self):
        return self.power_supply_name

class Case_model(models.Model):
    case_name = models.TextField(max_length=100)
    case_manufacturer = models.TextField(max_length=100)
    case_form_factor = models.CharField(max_length=100)
    case_size = models.CharField(max_length=100)
    case_power_supply_form_factor = models.CharField(max_length=50)
    case_fan = models.IntegerField()
    case_price = models.IntegerField()
    case_description = models.TextField(max_length=1500, blank=True)
    case_featured = models.BooleanField(default=True)
    case_image = models.ImageField(default='fallback.png', blank=True)

    def __str__(self):
        return self.case_name

class Computer_build(models.Model):
    build_name = models.TextField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    cpu = models.ForeignKey(Cpu_model, on_delete=models.CASCADE)
    motherboard = models.ForeignKey(Motherboard_model, on_delete=models.CASCADE)
    gpu = models.ForeignKey(Gpu_model, on_delete=models.CASCADE)
    ram = models.ForeignKey(Ram_model, on_delete=models.CASCADE)
    storage = models.ForeignKey(Storage_model, on_delete=models.CASCADE)
    cooling_system = models.ForeignKey(Cooling_system_model, on_delete=models.CASCADE)
    power_supply = models.ForeignKey(Power_supply_model, on_delete=models.CASCADE)
    case = models.ForeignKey(Case_model, on_delete=models.CASCADE)
    featured = models.BooleanField(default=True)
    price = models.IntegerField()

    def __str__(self):
        return self.build_name

