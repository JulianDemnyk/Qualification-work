from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden

from .filters import *
from .models import *


def home_view(request, *args, **kwargs):
    return render (request, "pages/base.html")


def compatibility_page(request):
    return render(request, 'items/compatibility_page.html')


def get_compatible_components(request):
    selected_cpu_id = request.GET.get('cpu_id')
    selected_motherboard_id = request.GET.get('motherboard_id')
    selected_gpu_id = request.GET.get('gpu_id')
    selected_ram_id = request.GET.get('ram_id')
    selected_cooling_system_id = request.GET.get('cooling_system_id')
    selected_power_supply_id = request.GET.get('power_supply_id')
    selected_storage_id = request.GET.get('storage_id')
    selected_case_id = request.GET.get('case_id')

    compatible_cpus = Cpu_model.objects.all()
    compatible_motherboards = Motherboard_model.objects.all()
    compatible_gpus = Gpu_model.objects.all()
    compatible_ram = Ram_model.objects.all()
    compatible_cooling_systems = Cooling_system_model.objects.all()
    compatible_power_supply = Power_supply_model.objects.all()
    compatible_cases = Case_model.objects.all()
    compatible_storages = Storage_model.objects.all()

    total_power_requirement = 175

    if selected_cpu_id:
        selected_cpu = get_object_or_404(Cpu_model, id=selected_cpu_id)
        compatible_motherboards = compatible_motherboards.filter(motherboard_socket=selected_cpu.cpu_socket)

        compatible_cooling_systems = compatible_cooling_systems.filter(
            cooling_system_socket__iregex=rf'\b{selected_cpu.cpu_socket}\b',
            cooling_system_tdp__gte=selected_cpu.cpu_tdp
        )

        total_power_requirement += selected_cpu.cpu_power_consumption

        compatible_cpus = compatible_cpus.filter(id=selected_cpu_id)

    if selected_motherboard_id:
        selected_motherboard = get_object_or_404(Motherboard_model, id=selected_motherboard_id)
        compatible_cpus = compatible_cpus.filter(cpu_socket=selected_motherboard.motherboard_socket)

        compatible_ram = compatible_ram.filter(
            ram_type=selected_motherboard.motherboard_ram_type,
            ram_amount__lte=selected_motherboard.motherboard_ram_slot
        )

        compatible_cooling_systems = compatible_cooling_systems.filter(
            cooling_system_socket__iregex=rf'\b{selected_motherboard.motherboard_socket}\b'
        )

        compatible_cases = compatible_cases.filter(
            case_form_factor__iregex=rf'\b{selected_motherboard.motherboard_form_factor}\b'
        )

        compatible_motherboards = compatible_motherboards.filter(id=selected_motherboard_id)

    if selected_ram_id:
        selected_ram = get_object_or_404(Ram_model, id=selected_ram_id)
        compatible_motherboards = compatible_motherboards.filter(
            motherboard_ram_type=selected_ram.ram_type,
            motherboard_ram_slot__gte=selected_ram.ram_amount
        )

        compatible_ram = compatible_ram.filter(id=selected_ram_id)

    if selected_cooling_system_id:
        selected_cooling_system = get_object_or_404(Cooling_system_model, id=selected_cooling_system_id)
        cooling_system_sockets = [socket.strip() for socket in selected_cooling_system.cooling_system_socket.split(',')]

        compatible_motherboards = compatible_motherboards.filter(
            motherboard_socket__in=cooling_system_sockets
        )

        compatible_cpus = compatible_cpus.filter(
            cpu_socket__in=cooling_system_sockets,
            cpu_tdp__lte=selected_cooling_system.cooling_system_tdp
        )

        total_power_requirement += selected_cooling_system.cooling_system_tdp/20

        compatible_cooling_systems = compatible_cooling_systems.filter(id=selected_cooling_system_id)

    if selected_gpu_id:
        selected_gpu = get_object_or_404(Gpu_model, id=selected_gpu_id)
        total_power_requirement += selected_gpu.gpu_power_consumption

        compatible_gpus = compatible_gpus.filter(id=selected_gpu_id)

    if selected_storage_id:
        get_object_or_404(Storage_model, id=selected_storage_id)

        compatible_storages = compatible_storages.filter(id=selected_storage_id)

    if selected_power_supply_id:
        selected_power_supply = get_object_or_404(Power_supply_model, id=selected_power_supply_id)

        if selected_power_supply.power_supply_power > total_power_requirement:
            compatible_power_supply = compatible_power_supply.filter(id=selected_power_supply_id)
        else:
            compatible_power_supply = compatible_power_supply.exclude(id=selected_power_supply_id)

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
                'featured': cpu.cpu_featured,
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
                'featured': motherboard.motherboard_featured,
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
                'featured': ram.ram_featured,
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
                'featured': cooling_system.cooling_system_featured,
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
                'featured': gpu.gpu_featured,
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
                'featured': power_supply.power_supply_featured,
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
                'featured': case.case_featured,
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
                'featured': storage.storage_featured,
                'image_url': storage.storage_image.url,
            }
            for storage in compatible_storages
        ]
    })


@login_required(login_url='login/')
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
        build_name = request.POST.get('build_name', '')

        if not all([cpu_id, motherboard_id, gpu_id, ram_id, storage_id, cooling_system_id, power_supply_id, case_id]):
            return JsonResponse({'status': 'error', 'message': 'All items must be selected'})

        try:
            cpu = Cpu_model.objects.get(id=cpu_id)
            motherboard = Motherboard_model.objects.get(id=motherboard_id)
            gpu = Gpu_model.objects.get(id=gpu_id)
            ram = Ram_model.objects.get(id=ram_id)
            storage = Storage_model.objects.get(id=storage_id)
            cooling_system = Cooling_system_model.objects.get(id=cooling_system_id)
            power_supply = Power_supply_model.objects.get(id=power_supply_id)
            case = Case_model.objects.get(id=case_id)

            total_price = (
                cpu.cpu_price + motherboard.motherboard_price + gpu.gpu_price + ram.ram_price + storage.storage_price
                + cooling_system.cooling_system_price + power_supply.power_supply_price + case.case_price
            )

            Computer_build.objects.create(
                build_name=build_name, owner=request.user,
                cpu=cpu, motherboard=motherboard, gpu=gpu, ram=ram,
                storage=storage, cooling_system=cooling_system, power_supply=power_supply, case=case,
                price=total_price
            )

            return JsonResponse({'status': 'success', 'message': 'Build saved successfully'})
        except Exception:
            return JsonResponse({'status': 'error', 'message': 'Something went wrong, please try again later'})


def detail_view_cpu(request, id):
    cpu = get_object_or_404(Cpu_model, id=id)
    context = {
        'cpu': cpu,
    }
    return render(request, 'items/items_detail/cpu_detail.html', context)


def list_view_cpu(request):
    cpus = Cpu_model.objects.filter(cpu_featured=True)
    f = CpuFilter(request.GET, queryset=cpus)

    context = {
        'filter': f,
        'cpu_list': f.qs,
        'cpu_count': f.qs.count(),
    }
    return render(request, "items/items_list/cpu_list.html", context)



def detail_view_motherboard(request, id):
    motherboard = get_object_or_404(Motherboard_model, id=id)
    context = {
        'motherboard': motherboard,
    }
    return render(request, 'items/items_detail/motherboard_detail.html', context)


def list_view_motherboard(request):
    motherboards = Motherboard_model.objects.filter(motherboard_featured=True)
    f = MotherboardFilter(request.GET, queryset=motherboards)

    context = {
        'filter': f,
        'motherboard_list': f.qs,
        'motherboard_count': f.qs.count(),
    }
    return render(request, "items/items_list/motherboard_list.html", context)


def detail_view_gpu(request, id):
    gpu = get_object_or_404(Gpu_model, id=id)
    context = {
        'gpu': gpu,
    }
    return render(request, 'items/items_detail/gpu_detail.html', context)


def list_view_gpu(request):
    gpus = Gpu_model.objects.filter(gpu_featured=True)
    f = GpuFilter(request.GET, queryset=gpus)

    context = {
        'filter': f,
        'gpu_list': f.qs,
        'gpu_count': f.qs.count(),
    }
    return render(request, "items/items_list/gpu_list.html", context)


def detail_view_ram(request, id):
    ram = get_object_or_404(Ram_model, id=id)
    context = {
        'ram': ram,
    }
    return render(request, 'items/items_detail/ram_detail.html', context)


def list_view_ram(request):
    rams = Ram_model.objects.filter(ram_featured=True)
    f = RamFilter(request.GET, queryset=rams)

    context = {
        'filter': f,
        'ram_list': f.qs,
        'ram_count': f.qs.count(),
    }
    return render(request, "items/items_list/ram_list.html", context)


def detail_view_storage(request, id):
    storage = get_object_or_404(Storage_model, id=id)
    context = {
        'storage': storage,
    }
    return render(request, 'items/items_detail/storage_detail.html', context)


def list_view_storage(request):
    storages = Storage_model.objects.filter(storage_featured=True)
    f = StorageFilter(request.GET, queryset=storages)

    context = {
        'filter': f,
        'storage_list': f.qs,
        'storage_count': f.qs.count(),
    }
    return render(request, "items/items_list/storage_list.html", context)


def detail_view_cooling_system(request, id):
    cooling_system = get_object_or_404(Cooling_system_model, id=id)
    context = {
        'cooling_system': cooling_system,
    }
    return render(request, 'items/items_detail/cooling_system_detail.html', context)


def list_view_cooling_system(request):
    coolings = Cooling_system_model.objects.filter(cooling_system_featured=True)
    f = CoolingSystemFilter(request.GET, queryset=coolings)

    context = {
        'filter': f,
        'cooling_list': f.qs,
        'cooling_count': f.qs.count(),
    }
    return render(request, "items/items_list/cooling_system_list.html", context)



def detail_view_power_supply(request, id):
    power_supply = get_object_or_404(Power_supply_model, id=id)
    context = {
        'power_supply': power_supply,
    }
    return render(request, 'items/items_detail/power_supply_detail.html', context)


def list_view_power_supply(request):
    power_supplies = Power_supply_model.objects.filter(power_supply_featured=True)
    f = PowerSupplyFilter(request.GET, queryset=power_supplies)

    context = {
        'filter': f,
        'power_supply_list': f.qs,
        'power_supply_count': f.qs.count(),
    }
    return render(request, "items/items_list/power_supply_list.html", context)


def detail_view_case(request, id):
    case = get_object_or_404(Case_model, id=id)
    context = {
        'case': case,
    }
    return render(request, 'items/items_detail/case_detail.html', context)


def list_view_case(request):
    cases = Case_model.objects.filter(case_featured=True)
    f = CaseFilter(request.GET, queryset=cases)

    context = {
        'filter': f,
        'case_list': f.qs,
        'case_count': f.qs.count(),
    }
    return render(request, "items/items_list/case_list.html", context)



def list_view_computer_build(request):
    builds_qs = Computer_build.objects.filter(owner__is_superuser=True, featured=True)
    f = ComputerBuildFilter(request.GET, queryset=builds_qs)

    context = {
        'filter': f,
        'builds': f.qs,
        'builds_count': f.qs.count(),
    }
    return render(request, 'items/computers/computer_build.html', context)


@login_required(login_url='login/')
def detail_view_build_profile(request, id):
    build = get_object_or_404(Computer_build, id=id)
    context = {
        'build': build,
    }
    return render(request, 'items/computers/computer_build_detail.html', context)


def detail_view_build(request, id):
    build = get_object_or_404(Computer_build.objects.filter(featured=True), id=id)
    context = {
        'build': build,
    }
    return render(request, 'items/computers/computer_build_detail.html', context)


def delete_view_computer_build(request, id):
    build = get_object_or_404(Computer_build, id=id)

    if request.user != build.owner and not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to do this action.")

    if request.method == 'POST':
        build.delete()
        return redirect('../')

    context = {
        'build': build,
    }
    return render(request, 'items/computers/computer_delete.html', context)


@login_required(login_url='login/')
def user_profile(request):
    builds = Computer_build.objects.filter(owner=request.user)
    f = ComputerBuildFilter(request.GET, queryset=builds)

    context = {
        'filter': f,
        'builds': f.qs,
        'builds_count': f.qs.count(),
    }
    return render(request, "pages/profile.html", context)


def login_page(request):
    page='login'

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect.')

    context = {
        'page': page,
    }
    return render(request, 'pages/login_sign_up.html', context)

    
def sign_up_page(request):
    page = 'sign_up'

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    context = {
        'page': page,
        'form': form,
    }
    return render(request, 'pages/login_sign_up.html', context)


def logout_page(request):
    logout(request)
    return redirect('home')