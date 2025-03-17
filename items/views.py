from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Motherboard_model, Cpu_model, Ram_model, Cooling_system_model, Gpu_model, Power_supply_model, \
    Case_model, Storage_model, Computer_build


def home_view(request, *args, **kwargs):
    return render (request, "pages/base.html", {})

def compatibility_page(request):
    return render(request, 'items/compatibility_page.html', {})

def get_compatible_components(request):
    selected_cpu_id = request.GET.get('cpu_id')
    selected_motherboard_id = request.GET.get('motherboard_id')
    selected_ram_id = request.GET.get('ram_id')
    selected_cooling_system_id = request.GET.get('cooling_system_id')
    selected_gpu_id = request.GET.get('gpu_id')
    selected_power_supply_id = request.GET.get('power_supply_id')
    selected_case_id = request.GET.get('case_id')

    compatible_cpus = Cpu_model.objects.all()
    compatible_motherboards = Motherboard_model.objects.all()
    compatible_ram = Ram_model.objects.all()
    compatible_cooling_systems = Cooling_system_model.objects.all()
    compatible_gpus = Gpu_model.objects.all()
    compatible_power_supply = Power_supply_model.objects.all()
    compatible_cases = Case_model.objects.all()
    compatible_storages = Storage_model.objects.all()

    total_power_requirement = 100

    if selected_cpu_id:
        selected_cpu = get_object_or_404(Cpu_model, id=selected_cpu_id)
        compatible_motherboards = compatible_motherboards.filter(motherboard_socket=selected_cpu.cpu_socket)

        compatible_cooling_systems = compatible_cooling_systems.filter(
            Q(cooling_system_socket__icontains=selected_cpu.cpu_socket),
            cooling_system_tdp__gte=selected_cpu.cpu_tdp
        )

        total_power_requirement += selected_cpu.cpu_tdp

        compatible_cpus = compatible_cpus.filter(id=selected_cpu_id)

    # Filter items based on the selected motherboard
    if selected_motherboard_id:
        selected_motherboard = get_object_or_404(Motherboard_model, id=selected_motherboard_id)
        compatible_cpus = compatible_cpus.filter(cpu_socket=selected_motherboard.motherboard_socket)

        # Filter RAM based on motherboard compatibility
        compatible_ram = compatible_ram.filter(
            ram_type=selected_motherboard.motherboard_ram_type,
            ram_amount__lte=selected_motherboard.motherboard_ram_slot
        )

        compatible_cooling_systems = compatible_cooling_systems.filter(
            Q(cooling_system_socket__icontains=selected_motherboard.motherboard_socket)
        )

        compatible_cases = compatible_cases.filter(
            Q(case_form_factor__icontains=selected_motherboard.motherboard_form_factor)
        )

        compatible_motherboards = compatible_motherboards.filter(id=selected_motherboard_id)

    # Filter based on selected RAM
    if selected_ram_id:
        selected_ram = get_object_or_404(Ram_model, id=selected_ram_id)
        compatible_motherboards = compatible_motherboards.filter(
            motherboard_ram_type=selected_ram.ram_type,
            motherboard_ram_slot__gte=selected_ram.ram_amount
        )

        compatible_ram = compatible_ram.filter(id=selected_ram_id)

    # Filter based on selected cooling system
    if selected_cooling_system_id:
        selected_cooling_system = get_object_or_404(Cooling_system_model, id=selected_cooling_system_id)
        cooling_system_sockets = [socket.strip() for socket in selected_cooling_system.cooling_system_socket.split(',')]

        compatible_motherboards = compatible_motherboards.filter(
            motherboard_socket__in=cooling_system_sockets
        )

        compatible_cpus = compatible_cpus.filter(
            cpu_socket__in=cooling_system_sockets, cpu_tdp__lte=selected_cooling_system.cooling_system_tdp
        )

        total_power_requirement += selected_cooling_system.cooling_system_tdp

        compatible_cooling_systems = compatible_cooling_systems.filter(id=selected_cooling_system_id)

    # Filter based on selected GPU
    if selected_gpu_id:
        selected_gpu = get_object_or_404(Gpu_model, id=selected_gpu_id)
        total_power_requirement += selected_gpu.gpu_power_consumption
        compatible_power_supply = compatible_power_supply.filter(
            power_supply_power__gt=total_power_requirement + selected_gpu.gpu_power_consumption
        )
        compatible_gpus = compatible_gpus.filter(id=selected_gpu_id)

    # Filter based on selected PSU
    if selected_power_supply_id:
        selected_power_supply = get_object_or_404(Power_supply_model, id=selected_power_supply_id)
        compatible_gpus = compatible_gpus.filter(gpu_power_consumption__lt=selected_power_supply.power_supply_power)
        compatible_power_supply = compatible_power_supply.filter(id=selected_power_supply_id)

    if selected_case_id:
        selected_case = get_object_or_404(Case_model, id=selected_case_id)
        case_form_factors = [form_factor.strip() for form_factor in selected_case.case_form_factor.split(',')]

        compatible_motherboards = compatible_motherboards.filter(motherboard_form_factor__in=case_form_factors)

        compatible_power_supply = compatible_power_supply.filter(power_supply_form_factor=selected_case.case_power_supply_form_factor)

        compatible_cases = compatible_cases.filter(id=selected_case_id)

    return JsonResponse({
        'cpus': [
            {
                'id': cpu.id,
                'name': cpu.cpu_name,
                'socket': cpu.cpu_socket,
                'price': cpu.cpu_price,
                'image_url': cpu.cpu_image.url,
            }
            for cpu in compatible_cpus
        ],
        'motherboards': [
            {
                'id': motherboard.id,
                'name': motherboard.motherboard_name,
                'socket': motherboard.motherboard_socket,
                'price': motherboard.motherboard_price,
                'image_url': motherboard.motherboard_image.url,
            }
            for motherboard in compatible_motherboards
        ],
        'rams': [
            {
                'id': ram.id,
                'name': ram.ram_name,
                'type': ram.ram_type,
                'amount': ram.ram_amount,
                'price': ram.ram_price,
                'image_url': ram.ram_image.url,
            }
            for ram in compatible_ram
        ],
        'cooling_systems': [
            {
                'id': cooling_system.id,
                'name': cooling_system.cooling_system_name,
                'socket': cooling_system.cooling_system_socket,
                'price': cooling_system.cooling_system_price,
                'image_url': cooling_system.cooling_system_image.url,
            }
            for cooling_system in compatible_cooling_systems
        ],
        'gpus': [
            {
                'id': gpu.id,
                'name': gpu.gpu_name,
                'ram': gpu.gpu_ram,
                'ram_type': gpu.gpu_ram_type,
                'bits': gpu.gpu_bits,
                'price': gpu.gpu_price,
                'image_url': gpu.gpu_image.url,
            }
            for gpu in compatible_gpus
        ],
        'power_supplys': [
            {
                'id': power_supply.id,
                'name': power_supply.power_supply_name,
                'power': power_supply.power_supply_power,
                'price': power_supply.power_supply_price,
                'image_url': power_supply.power_supply_image.url,
            }
            for power_supply in compatible_power_supply
        ],
        'cases': [
            {
                'id': case.id,
                'name': case.case_name,
                'size': case.case_size,
                'price': case.case_price,
                'image_url': case.case_image.url,
            }
            for case in compatible_cases
        ],
        'storages': [
            {
                'id': storage.id,
                'name': storage.storage_name,
                'type': storage.storage_type,
                'capacity': storage.storage_capacity,
                'speed': storage.storage_speed,
                'price': storage.storage_price,
                'image_url': storage.storage_image.url,
            }
            for storage in compatible_storages
        ]
    })


def save_computer_build(request):
    if request.method == 'POST':
        cpu_id = request.POST.get('cpu')
        motherboard_id = request.POST.get('motherboard')
        gpu_id = request.POST.get('gpu')
        ram_id = request.POST.get('ram')
        storage_id = request.POST.get('storage')
        cooling_system_id = request.POST.get('cooling_system')
        power_supply_id = request.POST.get('power_supply')
        case_id = request.POST.get('case')

        # Validate that all items are selected
        if not all([cpu_id, motherboard_id, gpu_id, ram_id, storage_id, cooling_system_id, power_supply_id, case_id]):
            return JsonResponse({'status': 'error', 'message': 'All items must be selected'})

        # Get the component objects from the database
        try:
            cpu = Cpu_model.objects.get(id=cpu_id)
            motherboard = Motherboard_model.objects.get(id=motherboard_id)
            gpu = Gpu_model.objects.get(id=gpu_id)
            ram = Ram_model.objects.get(id=ram_id)
            storage = Storage_model.objects.get(id=storage_id)
            cooling_system = Cooling_system_model.objects.get(id=cooling_system_id)
            power_supply = Power_supply_model.objects.get(id=power_supply_id)
            case = Case_model.objects.get(id=case_id)

            # Calculate total price
            total_price = (
                cpu.cpu_price + motherboard.motherboard_price + gpu.gpu_price +
                ram.ram_price + storage.storage_price + cooling_system.cooling_system_price +
                power_supply.power_supply_price + case.case_price
            )

            # Save the build to the database
            build = Computer_build.objects.create(
                owner=request.user,
                cpu=cpu,
                motherboard=motherboard,
                gpu=gpu,
                ram=ram,
                storage=storage,
                cooling_system=cooling_system,
                power=power_supply,
                case=case,
                price=total_price
            )

            return JsonResponse({'status': 'success', 'message': 'Build saved successfully', 'build_id': build.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def detail_view_cpu(request, id):
    cpu = get_object_or_404(Cpu_model, id=id)
    context = {
        'cpu': cpu,
    }
    return render(request, 'items/detail/cpu_detail.html', context)

def list_view_cpu(request):
    q=request.GET.get('q') if request.GET.get('q') is not None else ''

    cpu = Cpu_model.objects.filter(
        Q(cpu_name__contains=q)|
        Q(cpu_manufacturer__contains=q)|
        Q(cpu_socket__contains=q)|
        Q(cpu_description__contains=q)
    )

    cpu_count = cpu.count()

    context = {
        'cpu_list': cpu,
        'cpu_count': cpu_count,
    }
    return render(request, "items/list/cpu_list.html", context)

def detail_view_motherboard(request, id):
    motherboard = get_object_or_404(Motherboard_model, id=id)
    context = {
        'motherboard': motherboard,
    }
    return render(request, 'items/detail/motherboard_detail.html', context)

def list_view_motherboard(request):
    q=request.GET.get('q') if request.GET.get('q') is not None else ''

    motherboard = Motherboard_model.objects.filter(
        Q(motherboard_name__contains=q)|
        Q(motherboard_manufacturer__contains=q)|
        Q(motherboard_socket__contains=q)|
        Q(motherboard_chipset__contains=q) |
        Q(motherboard_form_factor__contains=q) |
        Q(motherboard_ram_type__contains=q) |
        Q(motherboard_description__contains=q)
    )

    motherboard_count = motherboard.count()

    context = {
        'motherboard_list': motherboard,
        'motherboard_count': motherboard_count,
    }
    return render(request, "items/list/motherboard_list.html", context)

def detail_view_gpu(request, id):
    gpu = get_object_or_404(Gpu_model, id=id)
    context = {
        'gpu': gpu,
    }
    return render(request, 'items/detail/gpu_detail.html', context)

def list_view_gpu(request):
    q=request.GET.get('q') if request.GET.get('q') is not None else ''

    gpu = Gpu_model.objects.filter(
        Q(gpu_name__contains=q)|
        Q(gpu_manufacturer__contains=q)|
        Q(gpu_ram_type__contains=q)|
        Q(gpu_description__contains=q)
    )

    gpu_count = gpu.count()

    context = {
        'gpu_list': gpu,
        'gpu_count': gpu_count,
    }
    return render(request, "items/list/gpu_list.html", context)

def detail_view_ram(request, id):
    ram = get_object_or_404(Ram_model, id=id)
    context = {
        'ram': ram,
    }
    return render(request, 'items/detail/ram_detail.html', context)

def list_view_ram(request):
    q=request.GET.get('q') if request.GET.get('q') is not None else ''

    ram = Ram_model.objects.filter(
        Q(ram_name__contains=q)|
        Q(ram_manufacturer__contains=q)|
        Q(ram_type__contains=q)|
        Q(ram_size__contains=q)|
        Q(ram_amount__contains=q) |
        Q(ram_description__contains=q)
    )

    ram_count = ram.count()

    context = {
        'ram_list': ram,
        'ram_count': ram_count,
    }
    return render(request, "items/list/ram_list.html", context)

def detail_view_storage(request, id):
    storage = get_object_or_404(Storage_model, id=id)
    context = {
        'storage': storage,
    }
    return render(request, 'items/detail/storage_detail.html', context)

def list_view_storage(request):
    q=request.GET.get('q') if request.GET.get('q') is not None else ''

    storage = Storage_model.objects.filter(
        Q(storage_name__contains=q)|
        Q(storage_manufacturer__contains=q)|
        Q(storage_type__contains=q)|
        Q(storage_capacity__contains=q)|
        Q(storage_connection__contains=q) |
        Q(storage_description__contains=q)
    )

    storage_count = storage.count()

    context = {
        'storage_list': storage,
        'storage_count': storage_count,
    }
    return render(request, "items/list/storage_list.html", context)

def detail_view_cooling_system(request, id):
    cooling_system = get_object_or_404(Cooling_system_model, id=id)
    context = {
        'cooling_system': cooling_system,
    }
    return render(request, 'items/detail/cooling_system_detail.html', context)

def list_view_cooling_system(request):
    q=request.GET.get('q') if request.GET.get('q') is not None else ''

    cooling_system = Cooling_system_model.objects.filter(
        Q(cooling_system_name__contains=q)|
        Q(cooling_system_manufacturer__contains=q)|
        Q(cooling_system_socket__contains=q)|
        Q(cooling_system_tdp__contains=q)|
        Q(cooling_system_description__contains=q)
    )

    cooling_system_count = cooling_system.count()

    context = {
        'cooling_system_list': cooling_system,
        'cooling_system_count': cooling_system_count,
    }
    return render(request, "items/list/cooling_system_list.html", context)

def detail_view_power_supply(request, id):
    power_supply = get_object_or_404(Power_supply_model, id=id)
    context = {
        'power_supply': power_supply,
    }
    return render(request, 'items/detail/power_supply_detail.html', context)

def list_view_power_supply(request):
    q=request.GET.get('q') if request.GET.get('q') is not None else ''

    power_supply = Power_supply_model.objects.filter(
        Q(power_supply_name__contains=q)|
        Q(power_supply_manufacturer__contains=q)|
        Q(power_supply_power__contains=q)|
        Q(power_supply_form_factor__contains=q)|
        Q(power_supply_description__contains=q)
    )

    power_supply_count = power_supply.count()

    context = {
        'power_supply_list': power_supply,
        'power_supply_count': power_supply_count,
    }
    return render(request, "items/list/power_supply_list.html", context)

def detail_view_case(request, id):
    case = get_object_or_404(Case_model, id=id)
    context = {
        'case': case,
    }
    return render(request, 'items/detail/case_detail.html', context)

def list_view_case(request):
    q=request.GET.get('q') if request.GET.get('q') is not None else ''

    case = Case_model.objects.filter(
        Q(case_name__contains=q)|
        Q(case_manufacturer__contains=q)|
        Q(case_size__contains=q)|
        Q(case_form_factor__contains=q)|
        Q(case_description__contains=q)
    )

    case_count = case.count()

    context = {
        'case_list': case,
        'case_count': case_count,
    }
    return render(request, "items/list/case_list.html", context)

def user_profile(request):
    builds = Computer_build.objects.filter(owner=request.user)
    context = {
        'builds': builds,
    }
    return render(request, "pages/profile.html", context)

def detail_view_build(request, id):
    build = get_object_or_404(Computer_build, id=id)
    context = {
        'build': build,
    }
    return render(request, 'items/detail/computer_build_detail.html', context)