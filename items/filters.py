import django_filters
from django.db.models import Q
from .models import *


class ComputerBuildFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='custom_search', label='Search')

    def custom_search(self, queryset, name, value):
        return queryset.filter(
            Q(build_name__icontains=value) |
            Q(cpu__cpu_name__icontains=value) |
            Q(cpu__cpu_manufacturer__icontains=value) |
            Q(cpu__cpu_socket__icontains=value) |
            Q(motherboard__motherboard_name__icontains=value) |
            Q(motherboard__motherboard_manufacturer__icontains=value) |
            Q(motherboard__motherboard_socket__icontains=value) |
            Q(motherboard__motherboard_chipset__icontains=value) |
            Q(motherboard__motherboard_form_factor__icontains=value) |
            Q(motherboard__motherboard_ram_type__icontains=value) |
            Q(gpu__gpu_name__icontains=value) |
            Q(gpu__gpu_manufacturer__icontains=value) |
            Q(gpu__gpu_ram__icontains=value) |
            Q(gpu__gpu_ram_type__icontains=value) |
            Q(ram__ram_name__icontains=value) |
            Q(ram__ram_manufacturer__icontains=value) |
            Q(ram__ram_type__icontains=value) |
            Q(ram__ram_size__icontains=value) |
            Q(ram__ram_amount__icontains=value) |
            Q(storage__storage_name__icontains=value) |
            Q(storage__storage_manufacturer__icontains=value) |
            Q(storage__storage_type__icontains=value) |
            Q(storage__storage_capacity__icontains=value) |
            Q(cooling_system__cooling_system_name__icontains=value) |
            Q(cooling_system__cooling_system_manufacturer__icontains=value) |
            Q(cooling_system__cooling_system_tdp__icontains=value) |
            Q(power_supply__power_supply_name__icontains=value) |
            Q(power_supply__power_supply_manufacturer__icontains=value) |
            Q(power_supply__power_supply_power__icontains=value) |
            Q(power_supply__power_supply_form_factor__icontains=value) |
            Q(case__case_name__icontains=value) |
            Q(case__case_manufacturer__icontains=value) |
            Q(case__case_size__icontains=value)
        )

    cpu_manufacturer = django_filters.ChoiceFilter(
        choices = [(i, i) for i in Cpu_model.objects.values_list('cpu_manufacturer', flat=True).distinct()],
        field_name = 'cpu__cpu_manufacturer',
        empty_label='',
        label = 'Processor manufacturer'
    )

    cpu_type = django_filters.ChoiceFilter(
        choices = [(i, i) for i in Cpu_model.objects.values_list('cpu_type', flat=True).distinct()],
        field_name = 'cpu__cpu_type',
        empty_label='',
        label = 'Processor type'
    )

    cpu_socket = django_filters.ChoiceFilter(
        choices = [(i, i) for i in Cpu_model.objects.values_list('cpu_socket', flat=True).distinct()],
        field_name = 'cpu__cpu_socket',
        empty_label='',
        label = 'Processor socket'
    )

    motherboard_manufacturer = django_filters.ChoiceFilter(
        choices = [(i, i) for i in Motherboard_model.objects.values_list('motherboard_manufacturer', flat=True).distinct()],
        field_name = 'motherboard__motherboard_manufacturer',
        empty_label='',
        label = 'Motherboard manufacturer'
    )

    motherboard_socket = django_filters.ChoiceFilter(
        choices = [(i, i) for i in Motherboard_model.objects.values_list('motherboard_socket', flat=True).distinct()],
        field_name = 'motherboard__motherboard_socket',
        empty_label='',
        label = 'Motherboard manufacturer'
    )

    motherboard_chipset = django_filters.ChoiceFilter(
        choices = [(i, i) for i in Motherboard_model.objects.values_list('motherboard_chipset', flat=True).distinct()],
        field_name = 'motherboard__motherboard_chipset',
        empty_label='',
        label = 'Motherboard chipset'
    )

    motherboard_ram_type = django_filters.ChoiceFilter(
        choices = [(i, i) for i in Motherboard_model.objects.values_list('motherboard_ram_type', flat=True).distinct()],
        field_name = 'motherboard__motherboard_ram_type',
        empty_label='',
        label = 'Motherboard memory type'
    )

    gpu_manufacturer = django_filters.ChoiceFilter(
        choices = [(i, i) for i in Gpu_model.objects.values_list('gpu_manufacturer', flat=True).distinct()],
        field_name = 'gpu__gpu_manufacturer',
        empty_label='',
        label = 'Graphics card manufacturer'
    )

    gpu_chip = django_filters.ChoiceFilter(
        choices = [(i, i) for i in Gpu_model.objects.values_list('gpu_chip', flat=True).distinct()],
        field_name = 'gpu__gpu_chip',
        empty_label='',
        label = 'Graphics card chip'
    )

    gpu_ram = django_filters.ChoiceFilter(
        choices = [(i, i) for i in Gpu_model.objects.values_list('gpu_ram', flat=True).distinct()],
        field_name = 'gpu__gpu_ram',
        empty_label='',
        label = 'Graphics card memory'
    )

    ram_manufacturer = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Ram_model.objects.values_list('ram_manufacturer', flat=True).distinct()],
        field_name='ram__ram_manufacturer',
        empty_label='',
        label='Memory manufacturer'
    )

    ram_type = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Ram_model.objects.values_list('ram_type', flat=True).distinct()],
        field_name='ram__ram_type',
        empty_label='',
        label='Memory type'
    )

    ram_size = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Ram_model.objects.values_list('ram_size', flat=True).distinct()],
        field_name='ram__ram_size',
        empty_label='',
        label='Memory size'
    )

    ram_amount = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Ram_model.objects.values_list('ram_amount', flat=True).distinct()],
        field_name='ram__ram_amount',
        empty_label='',
        label='Memory amount'
    )

    storage_manufacturer = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Storage_model.objects.values_list('storage_manufacturer', flat=True).distinct()],
        field_name='storage__storage_manufacturer',
        empty_label='',
        label='Storage manufacturer'
    )

    storage_capacity = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Storage_model.objects.values_list('storage_capacity', flat=True).distinct()],
        field_name='storage__storage_capacity',
        empty_label='',
        label='Storage capacity'
    )

    storage_type = django_filters.ChoiceFilter(
        choices = [(i, i) for i in Storage_model.objects.values_list('storage_type', flat=True).distinct()],
        field_name = 'storage__storage_type',
        empty_label='',
        label = 'Storage type'
    )

    cooling_system_manufacturer = django_filters.ChoiceFilter(
        choices = [(i, i) for i in Cooling_system_model.objects.values_list('cooling_system_manufacturer', flat=True).distinct()],
        field_name = 'cooling_system__cooling_system_manufacturer',
        empty_label='',
        label = 'Cooling system manufacturer'
    )

    cooling_system_type = django_filters.ChoiceFilter(
        choices = [(i, i) for i in Cooling_system_model.objects.values_list('cooling_system_type', flat=True).distinct()],
        field_name = 'cooling_system__cooling_system_type',
        empty_label='',
        label = 'Cooling system type'
    )

    power_supply_manufacturer = django_filters.ChoiceFilter(
        choices = [(i, i) for i in Power_supply_model.objects.values_list('power_supply_manufacturer', flat=True).distinct()],
        field_name = 'power_supply__power_supply_manufacturer',
        empty_label='',
        label = 'Power supply manufacturer'
    )

    power_supply_power = django_filters.ChoiceFilter(
        choices = [(i, i) for i in Power_supply_model.objects.values_list('power_supply_power', flat=True).distinct()],
        field_name = 'power_supply__power_supply_power',
        empty_label='',
        label = 'Power supply power'
    )

    case_manufacturer = django_filters.ChoiceFilter(
        choices = [(i, i) for i in Case_model.objects.values_list('case_manufacturer', flat=True).distinct()],
        field_name = 'case__case_manufacturer',
        empty_label='',
        label = 'Case manufacturer'
    )

    case_size = django_filters.ChoiceFilter(
        choices = [(i, i) for i in Case_model.objects.values_list('case_size', flat=True).distinct()],
        field_name = 'case__case_size',
        empty_label='',
        label = 'Case size'
    )

class MotherboardFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='custom_search', label='Search')

    def custom_search(self, queryset, name, value):
        return queryset.filter(
            Q(motherboard_name__icontains=value) |
            Q(motherboard_manufacturer__icontains=value) |
            Q(motherboard_socket__icontains=value) |
            Q(motherboard_chipset__icontains=value) |
            Q(motherboard_form_factor__icontains=value) |
            Q(motherboard_ram_type__icontains=value)
        )

    motherboard_manufacturer = django_filters.ChoiceFilter(
        choices = [(i, i) for i in Motherboard_model.objects.values_list('motherboard_manufacturer', flat=True).distinct()],
        field_name = 'motherboard_manufacturer',
        empty_label='',
        label = 'Motherboard manufacturer'
    )

    motherboard_socket = django_filters.ChoiceFilter(
        choices = [(i, i) for i in Motherboard_model.objects.values_list('motherboard_socket', flat=True).distinct()],
        field_name = 'motherboard_socket',
        empty_label='',
        label = 'Motherboard socket'
    )

    motherboard_chipset = django_filters.ChoiceFilter(
        choices = [(i, i) for i in Motherboard_model.objects.values_list('motherboard_chipset', flat=True).distinct()],
        field_name = 'motherboard_chipset',
        empty_label='',
        label = 'Motherboard chipset'
    )

    motherboard_ram_type = django_filters.ChoiceFilter(
        choices = [(i, i) for i in Motherboard_model.objects.values_list('motherboard_ram_type', flat=True).distinct()],
        field_name = 'motherboard_ram_type',
        empty_label='',
        label = 'Motherboard memory type'
    )


class CpuFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='custom_search', label='Search')

    def custom_search(self, queryset, name, value):
        return queryset.filter(
            Q(cpu_name__icontains=value) |
            Q(cpu_manufacturer__icontains=value) |
            Q(cpu_type__icontains=value) |
            Q(cpu_socket__icontains=value) |
            Q(cpu_cores__icontains=value) |
            Q(cpu_threads__icontains=value) |
            Q(cpu_tdp__icontains=value)
        )

    cpu_manufacturer = django_filters.ChoiceFilter(
        choices = [(i, i) for i in Cpu_model.objects.values_list('cpu_manufacturer', flat=True).distinct()],
        field_name = 'cpu_manufacturer',
        empty_label='',
        label = 'Processor manufacturer'
    )

    cpu_socket = django_filters.ChoiceFilter(
        choices = [(i, i) for i in Cpu_model.objects.values_list('cpu_socket', flat=True).distinct()],
        field_name = 'cpu_socket',
        empty_label='',
        label = 'Processor manufacturer'
    )

    cpu_cores = django_filters.ChoiceFilter(
        choices = [(i, i) for i in Cpu_model.objects.values_list('cpu_cores', flat=True).distinct()],
        field_name = 'cpu_cores',
        empty_label='',
        label = 'Processor cores'
    )

    cpu_threads = django_filters.ChoiceFilter(
        choices = [(i, i) for i in Cpu_model.objects.values_list('cpu_threads', flat=True).distinct()],
        field_name = 'cpu_threads',
        empty_label='',
        label = 'Processor threads'
    )

    cpu_tdp = django_filters.ChoiceFilter(
        choices = [(i, i) for i in Cpu_model.objects.values_list('cpu_tdp', flat=True).distinct()],
        field_name = 'cpu_tdp',
        empty_label='',
        label = 'Processor thermal design power'
    )



class GpuFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='custom_search', label='Search')

    def custom_search(self, queryset, name, value):
        return queryset.filter(
            Q(gpu_name__icontains=value) |
            Q(gpu_manufacturer__icontains=value) |
            Q(gpu_chip__icontains=value) |
            Q(gpu_bit__icontains=value) |
            Q(gpu___icontains=value) |
            Q(cpu_threads__icontains=value) |
            Q(cpu_tdp__icontains=value) |
            Q(cpu_power_consumption__icontains=value)
        )

    cpu_manufacturer = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Cpu_model.objects.values_list('cpu_manufacturer', flat=True).distinct()],
        field_name='cpu_manufacturer',
        empty_label='',
        label='Processor manufacturer'
    )

    cpu_socket = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Cpu_model.objects.values_list('cpu_socket', flat=True).distinct()],
        field_name='cpu_socket',
        empty_label='',
        label='Processor manufacturer'
    )

    cpu_cores = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Cpu_model.objects.values_list('cpu_cores', flat=True).distinct()],
        field_name='cpu_cores',
        empty_label='',
        label='Processor cores'
    )

    cpu_threads = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Cpu_model.objects.values_list('cpu_threads', flat=True).distinct()],
        field_name='cpu_threads',
        empty_label='',
        label='Processor threads'
    )

    cpu_tdp = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Cpu_model.objects.values_list('cpu_tdp', flat=True).distinct()],
        field_name='cpu_tdp',
        empty_label='',
        label='Processor thermal design power'
    )

    cpu_power_consumption = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Cpu_model.objects.values_list('cpu_power_consumption', flat=True).distinct()],
        field_name='cpu_power_consumption',
        empty_label='',
        label='Processor power consumption'
    )

class GpuFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='custom_search', label='Search')

    def custom_search(self, queryset, name, value):
        return queryset.filter(
            Q(gpu_name__icontains=value) |
            Q(gpu_manufacturer__icontains=value) |
            Q(gpu_chip__icontains=value) |
            Q(gpu_clock_speed__icontains=value) |
            Q(gpu_ram__icontains=value) |
            Q(gpu_ram_type__icontains=value) |
            Q(gpu_description__icontains=value)
        )

    gpu_name = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Gpu_model.objects.values_list('gpu_name', flat=True).distinct()],
        field_name='gpu_name',
        empty_label='',
        label='Graphics card name'
    )

    gpu_manufacturer = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Gpu_model.objects.values_list('gpu_manufacturer', flat=True).distinct()],
        field_name='gpu_manufacturer',
        empty_label='',
        label='Graphics card manufacturer'
    )

    gpu_chip = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Gpu_model.objects.values_list('gpu_chip', flat=True).distinct()],
        field_name='gpu_chip',
        empty_label='',
        label='Graphics card chip'
    )

    gpu_bits = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Gpu_model.objects.values_list('gpu_bits', flat=True).distinct()],
        field_name='gpu_bits',
        empty_label='',
        label='Graphics card bits'
    )

    gpu_ram = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Gpu_model.objects.values_list('gpu_ram', flat=True).distinct()],
        field_name='gpu_ram',
        empty_label='',
        label='Graphics card memory size'
    )

    gpu_ram_type = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Gpu_model.objects.values_list('gpu_ram_type', flat=True).distinct()],
        field_name='gpu_ram_type',
        empty_label='',
        label='Graphics card memory type'
    )

class RamFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='custom_search', label='Search')

    def custom_search(self, queryset, name, value):
        return queryset.filter(
            Q(ram_name__icontains=value) |
            Q(ram_manufacturer__icontains=value) |
            Q(ram_type__icontains=value) |
            Q(ram_clock_speed__icontains=value) |
            Q(ram_size__icontains=value) |
            Q(ram_amount__icontains=value)
        )

    ram_name = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Ram_model.objects.values_list('ram_name', flat=True).distinct()],
        field_name='ram_name',
        empty_label='',
        label='Memory name'
    )

    ram_manufacturer = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Ram_model.objects.values_list('ram_manufacturer', flat=True).distinct()],
        field_name='ram_manufacturer',
        empty_label='',
        label='Memory manufacturer'
    )

    ram_type = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Ram_model.objects.values_list('ram_type', flat=True).distinct()],
        field_name='ram_type',
        empty_label='',
        label='Memory type'
    )

    ram_clock_speed = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Ram_model.objects.values_list('ram_clock_speed', flat=True).distinct()],
        field_name='ram_clock_speed',
        empty_label='',
        label='Memory clock speed'
    )

    ram_size = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Ram_model.objects.values_list('ram_size', flat=True).distinct()],
        field_name='ram_size',
        empty_label='',
        label='Memory size'
    )

    ram_amount = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Ram_model.objects.values_list('ram_amount', flat=True).distinct()],
        field_name='ram_amount',
        empty_label='',
        label='Memory amount of modules'
    )

class StorageFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='custom_search', label='Search')

    def custom_search(self, queryset, name, value):
        return queryset.filter(
            Q(storage_name__icontains=value) |
            Q(storage_manufacturer__icontains=value) |
            Q(storage_type__icontains=value) |
            Q(storage_capacity__icontains=value) |
            Q(storage_speed__icontains=value) |
            Q(storage_connection__icontains=value)
        )

    storage_name = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Storage_model.objects.values_list('storage_name', flat=True).distinct()],
        field_name='storage_name',
        empty_label='',
        label='Storage name'
    )

    storage_manufacturer = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Storage_model.objects.values_list('storage_manufacturer', flat=True).distinct()],
        field_name='storage_manufacturer',
        empty_label='',
        label='Storage manufacturer'
    )

    storage_type = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Storage_model.objects.values_list('storage_type', flat=True).distinct()],
        field_name='storage_type',
        empty_label='',
        label='Storage type'
    )

    storage_capacity = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Storage_model.objects.values_list('storage_capacity', flat=True).distinct()],
        field_name='storage_capacity',
        empty_label='',
        label='Storage capacity'
    )

    storage_speed = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Storage_model.objects.values_list('storage_speed', flat=True).distinct()],
        field_name='storage_speed',
        empty_label='',
        label='Storage upload speed'
    )

    storage_connection = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Storage_model.objects.values_list('storage_connection', flat=True).distinct()],
        field_name='storage_connection',
        empty_label='',
        label='Storage connection type'
    )


class CoolingSystemFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='custom_search', label='Search')

    def custom_search(self, queryset, name, value):
        return queryset.filter(
            Q(cooling_system_name__icontains=value) |
            Q(cooling_system_manufacturer__icontains=value) |
            Q(cooling_system_socket__icontains=value) |
            Q(cooling_system_tdp__icontains=value) |
            Q(cooling_system_type__icontains=value)
        )

    cooling_system_name = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Cooling_system_model.objects.values_list('cooling_system_name', flat=True).distinct()],
        field_name='cooling_system_name',
        empty_label='',
        label='Cooling system name'
    )

    cooling_system_manufacturer = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Cooling_system_model.objects.values_list('cooling_system_manufacturer', flat=True).distinct()],
        field_name='cooling_system_manufacturer',
        empty_label='',
        label='Cooling system manufacturer'
    )

    cooling_system_socket = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Cooling_system_model.objects.values_list('cooling_system_socket', flat=True).distinct()],
        field_name='cooling_system_socket',
        empty_label='',
        label='Cooling system socket'
    )

    cooling_system_type = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Cooling_system_model.objects.values_list('cooling_system_type', flat=True).distinct()],
        field_name='cooling_system_type',
        empty_label='',
        label='Cooling system type'
    )

    cooling_system_tdp = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Cooling_system_model.objects.values_list('cooling_system_tdp', flat=True).distinct()],
        field_name='cooling_system_tdp',
        empty_label='',
        label='Cooling system thermal design power'
    )

class PowerSupplyFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='custom_search', label='Search')

    def custom_search(self, queryset, name, value):
        return queryset.filter(
            Q(power_supply_name__icontains=value) |
            Q(power_supply_manufacturer__icontains=value) |
            Q(power_supply_form_factor__icontains=value) |
            Q(power_supply_power__icontains=value)
        )

    power_supply_name = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Power_supply_model.objects.values_list('power_supply_name', flat=True).distinct()],
        field_name='power_supply_name',
        empty_label='',
        label='Power supply name'
    )

    power_supply_manufacturer = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Power_supply_model.objects.values_list('power_supply_manufacturer', flat=True).distinct()],
        field_name='power_supply_manufacturer',
        empty_label='',
        label='Power supply manufacturer'
    )

    power_supply_form_factor = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Power_supply_model.objects.values_list('power_supply_form_factor', flat=True).distinct()],
        field_name='power_supply_form_factor',
        empty_label='',
        label='Power supply form factor'
    )

    power_supply_power = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Power_supply_model.objects.values_list('power_supply_power', flat=True).distinct()],
        field_name='power_supply_power',
        empty_label='',
        label='Power supply power'
    )

class CaseFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='custom_search', label='Search')

    def custom_search(self, queryset, name, value):
        return queryset.filter(
            Q(case_name__icontains=value) |
            Q(case_manufacturer__icontains=value) |
            Q(case_form_factor__icontains=value) |
            Q(case_size__icontains=value) |
            Q(case_fan__icontains=value)
        )

    case_name = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Case_model.objects.values_list('case_name', flat=True).distinct()],
        field_name='case_name',
        empty_label='',
        label='Case name'
    )

    case_manufacturer = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Case_model.objects.values_list('case_manufacturer', flat=True).distinct()],
        field_name='case_manufacturer',
        empty_label='',
        label='Case manufacturer'
    )

    case_form_factor = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Case_model.objects.values_list('case_form_factor', flat=True).distinct()],
        field_name='case_form_factor',
        empty_label='',
        label='Case form factor'
    )

    case_size = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Case_model.objects.values_list('case_size', flat=True).distinct()],
        field_name='case_size',
        empty_label='',
        label='Case size'
    )

    case_fan = django_filters.ChoiceFilter(
        choices=[(i, i) for i in Case_model.objects.values_list('case_fan', flat=True).distinct()],
        field_name='case_fan',
        empty_label='',
        label='Case fans'
    )