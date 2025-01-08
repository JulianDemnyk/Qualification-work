from django.db import models

# Create your models here.
class Motherboard_model(models.Model):
    motherboard_name = models.TextField(max_length=100)
    motherboard_manufacturer = models.CharField(max_length=100)
    motherboard_socket = models.TextField(max_length=10)
    motherboard_chipset = models.TextField(max_length=10)
    motherboard_ram_type = models.TextField(max_length=10)
    motherboard_ram_slot = models.IntegerField()
    motherboard_pci_slot = models.IntegerField()
    motherboard_sata_slot = models.IntegerField()
    motherboard_m2_slot = models.IntegerField()
    motherboard_form_factor = models.CharField(max_length=10)
    motherboard_description = models.TextField(max_length=500, blank=True)
    motherboard_image = models.ImageField(default='fallback.png', blank=True)

class Cpu_model(models.Model):
    cpu_name = models.TextField(max_length=100)
    cpu_manufacturer = models.TextField(max_length=100)
    cpu_socket = models.TextField(max_length=10)
    cpu_cores = models.IntegerField()
    cpu_threads = models.IntegerField()
    cpu_clock_speed = models.TextField(max_length=10)
    cpu_tdp = models.IntegerField()
    cpu_description = models.TextField(max_length=500, blank=True)
    cpu_image = models.ImageField(default='fallback.png', blank=True)

