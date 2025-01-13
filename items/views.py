from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Motherboard_model, Cpu_model, Ram_model

# Create your views here.

def compatibility_page(request):
    # Render the main compatibility page
    cpus = Cpu_model.objects.all()
    motherboards = Motherboard_model.objects.all()
    ram_modules = Ram_model.objects.all()
    return render(request, 'compatibility_page.html', {
        'cpus': cpus,
        'motherboards': motherboards,
        'ram_modules': ram_modules,
    })

# Handle compatibility filtering for components
def get_compatible_components(request):
    selected_cpu_id = request.GET.get('cpu_id')  # Get selected CPU ID from query params
    selected_motherboard_id = request.GET.get('motherboard_id')  # Get selected motherboard ID
    selected_ram_id = request.GET.get('ram_id')  # Get selected RAM ID

    compatible_cpus = Cpu_model.objects.all()
    compatible_motherboards = Motherboard_model.objects.all()
    compatible_ram = Ram_model.objects.all()

    # Filter components based on the selected CPU
    if selected_cpu_id:
        selected_cpu = get_object_or_404(Cpu_model, id=selected_cpu_id)
        compatible_motherboards = compatible_motherboards.filter(motherboard_socket=selected_cpu.cpu_socket)
        compatible_cpus = compatible_cpus.filter(id=selected_cpu_id)  # Keep only the selected CPU

    # Filter components based on the selected motherboard
    if selected_motherboard_id:
        selected_motherboard = get_object_or_404(Motherboard_model, id=selected_motherboard_id)
        compatible_cpus = compatible_cpus.filter(cpu_socket=selected_motherboard.motherboard_socket)
        compatible_motherboards = compatible_motherboards.filter(
            id=selected_motherboard_id)  # Keep only the selected motherboard

        # Filter RAM based on motherboard compatibility
        compatible_ram = compatible_ram.filter(
            ram_type=selected_motherboard.motherboard_ram_type,  # RAM type matches motherboard
            ram_amount__lte=selected_motherboard.motherboard_ram_slot  # RAM amount does not exceed slots
        )

    # Filter components based on the selected RAM
    if selected_ram_id:
        selected_ram = get_object_or_404(Ram_model, id=selected_ram_id)
        compatible_motherboards = compatible_motherboards.filter(motherboard_ram_type=selected_ram.ram_type,
                                                                 motherboard_ram_slot__gte=selected_ram.ram_amount)
        compatible_ram = compatible_ram.filter(id=selected_ram_id)  # Keep only the selected RAM

    return JsonResponse({
        'cpus': [
            {
                'id': cpu.id,
                'name': cpu.cpu_name,
                'socket': cpu.cpu_socket,
                'price': cpu.cpu_price,
                'image_url': cpu.cpu_image.url if cpu.cpu_image else None,
            }
            for cpu in compatible_cpus
        ],
        'motherboards': [
            {
                'id': mb.id,
                'name': mb.motherboard_name,
                'socket': mb.motherboard_socket,
                'price': mb.motherboard_price,
                'image_url': mb.motherboard_image.url if mb.motherboard_image else None,
            }
            for mb in compatible_motherboards
        ],
        'ram': [  # Change from 'ram_modules' to 'ram'
            {
                'id': ram.id,
                'name': ram.ram_name,
                'type': ram.ram_type,
                'amount': ram.ram_amount,
                'price': ram.ram_price,
                'image_url': ram.ram_image.url if ram.ram_image else None,
            }
            for ram in compatible_ram
        ],
    })

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