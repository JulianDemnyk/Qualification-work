from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Motherboard_model, Cpu_model, Ram_model, Cooling_system_model, Gpu_model, Power_supply_model, \
    Case_model, Storage_model, Computer_build


# Create your views here.

def compatibility_page(request):
    # Render the main compatibility page
    cpus = Cpu_model.objects.all()
    motherboards = Motherboard_model.objects.all()
    ram_modules = Ram_model.objects.all()
    cooling_systems = Cooling_system_model.objects.all()
    gpus = Gpu_model.objects.all()
    power_supplys = Power_supply_model.objects.all()
    cases = Case_model.objects.all()
    storages = Storage_model.objects.all()
    return render(request, 'compatibility_page.html', {
        'cpus': cpus,
        'motherboards': motherboards,
        'ram_modules': ram_modules,
        'cooling_systems': cooling_systems,
        'gpus': gpus,
        'power_supplys': power_supplys,
        'cases': cases,
        'storages': storages,
    })

# Handle compatibility filtering for components
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

    total_power_requirement = 200

    # Filter components based on the selected CPU
    if selected_cpu_id:
        selected_cpu = get_object_or_404(Cpu_model, id=selected_cpu_id)
        compatible_motherboards = compatible_motherboards.filter(motherboard_socket=selected_cpu.cpu_socket)

        compatible_cooling_systems = compatible_cooling_systems.filter(
            Q(cooling_system_socket__icontains=selected_cpu.cpu_socket),
            cooling_system_tdp__gte=selected_cpu.cpu_tdp
        )

        total_power_requirement += selected_cpu.cpu_tdp

        compatible_cpus = compatible_cpus.filter(id=selected_cpu_id)

    # Filter components based on the selected motherboard
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
        compatible_power_supply = compatible_power_supply.filter(
            power_supply_power__gt=total_power_requirement + selected_gpu.gpu_power_consumption
        )
        compatible_gpus = compatible_gpus.filter(id=selected_gpu_id)
        total_power_requirement += selected_gpu.gpu_power_consumption

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
                'id': mb.id,
                'name': mb.motherboard_name,
                'socket': mb.motherboard_socket,
                'price': mb.motherboard_price,
                'image_url': mb.motherboard_image.url,
            }
            for mb in compatible_motherboards
        ],
        'ram': [
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
                'id': cooling_sys.id,
                'name': cooling_sys.cooling_system_name,
                'socket': cooling_sys.cooling_system_socket,
                'price': cooling_sys.cooling_system_price,
                'image_url': cooling_sys.cooling_system_image.url,
            }
            for cooling_sys in compatible_cooling_systems
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
        'power_supply': [
            {
                'id': power_sup.id,
                'name': power_sup.power_supply_name,
                'power': power_sup.power_supply_power,
                'price': power_sup.power_supply_price,
                'image_url': power_sup.power_supply_image.url,
            }
            for power_sup in compatible_power_supply
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

        # Validate that all components are selected
        if not all([cpu_id, motherboard_id, gpu_id, ram_id, storage_id, cooling_system_id, power_supply_id, case_id]):
            return JsonResponse({'status': 'error', 'message': 'All components must be selected'})

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


def fetch_all_cpus(request):
    cpus = Cpu_model.objects.all()
    response = [
        {
            'id': cpu.id,
            'name': cpu.cpu_name,
            'socket': cpu.cpu_socket,
            'price': cpu.cpu_price,
            'image_url': cpu.cpu_image.url,
        }
        for cpu in cpus
    ]
    return JsonResponse({'cpus': response})

def fetch_all_motherboards(request):
    motherboards = Motherboard_model.objects.all()
    response = [
        {
            'id': mb.id,
            'name': mb.motherboard_name,
            'socket': mb.motherboard_socket,
            'price': mb.motherboard_price,
            'image_url': mb.motherboard_image.url,
        }
        for mb in motherboards
    ]
    return JsonResponse({'motherboards': response})

def fetch_all_rams(request):
    ram_modules = Ram_model.objects.all()
    response = [
        {
            'id': ram.id,
            'name': ram.ram_name,
            'type': ram.ram_type,
            'amount': ram.ram_amount,
            'price': ram.ram_price,
            'image_url': ram.ram_image.url,
        }
        for ram in ram_modules
    ]
    return JsonResponse({'ram_modules': response})

def fetch_all_cooling_systems(request):
    cooling_systems = Cooling_system_model.objects.all()
    response = [
        {
            'id': cooling_sys.id,
            'name': cooling_sys.cooling_system_name,
            'price': cooling_sys.cooling_system_price,
            'sockets': cooling_sys.cooling_system_socket,
            'image_url': cooling_sys.cooling_system_image.url,
        }
        for cooling_sys in cooling_systems
    ]
    return JsonResponse({'cooling_systems': response})

def fetch_all_gpus(request):
    gpus = Gpu_model.objects.all()
    response = [
        {
            'id': gpu.id,
            'name': gpu.gpu_name,
            'ram': gpu.gpu_ram,
            'ram_type': gpu.gpu_ram_type,
            'bits': gpu.gpu_bits,
            'price': gpu.gpu_price,
            'image_url': gpu.gpu_image.url,
        }
        for gpu in gpus
    ]
    return JsonResponse({'gpus': response})

def fetch_all_power_supplies(request):
    power_supply = Power_supply_model.objects.all()
    response = [
        {
            'id': power_sup.id,
            'name': power_sup.power_supply_name,
            'power': power_sup.power_supply_power,
            'price': power_sup.power_supply_price,
            'image_url': power_sup.power_supply_image.url,
        }
        for power_sup in power_supply
    ]
    return JsonResponse({'power_supply': response})

def fetch_all_cases(request):
    cases = Case_model.objects.all()
    response = [
        {
            'id': case.id,
            'name': case.case_name,
            'size': case.case_size,
            'price': case.case_price,
            'image_url': case.case_image.url,
        }
        for case in cases
    ]
    return JsonResponse({'cases': response})

def fetch_all_storages(request):
    storages = Storage_model.objects.all()
    response = [
        {
            'id': storage.id,
            'name': storage.storage_name,
            'type': storage.storage_type,
            'capacity': storage.storage_capacity,
            'speed': storage.storage_speed,
            'price': storage.storage_price,
            'image_url': storage.storage_image.url,
        }
        for storage in storages
    ]
    return JsonResponse({'storages': response})