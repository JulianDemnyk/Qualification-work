let selectedCPU = null;
let selectedMotherboard = null;
let selectedRAM = null;
let selectedCoolingSystem = null;
let selectedGPU = null;
let selectedPowerSupply = null;
let selectedStorage = null;
let selectedCase = null;

let totalPrice = 0;

function fetchComponents() {
    const url = '/get_compatible_components/';
    const data = {
        cpu_id: selectedCPU,
        motherboard_id: selectedMotherboard,
        ram_id: selectedRAM,
        cooling_system_id: selectedCoolingSystem,
        gpu_id: selectedGPU,
        power_supply_id: selectedPowerSupply,
        storage_id: selectedStorage,
        case_id: selectedCase
    };
    $.ajax({
        url: url,
        data: data,
        success: function (response) {
            updateComponentList('cpu', response.cpus);
            updateComponentList('motherboard', response.motherboards); // Ensure this is updated
            updateComponentList('ram', response.rams);
            updateComponentList('cooling_system', response.cooling_systems);
            updateComponentList('gpu', response.gpus);
            updateComponentList('power_supply', response.power_supplys);
            updateComponentList('storage', response.storages);
            updateComponentList('case', response.cases);
        },
    });
}

function updateComponentList(type, components) {
    const listContainer = type === 'cpu' ? $('#cpu-list') :
        type === 'motherboard' ? $('#motherboard-list') :
            type === 'ram' ? $('#ram-list') :
                type === 'cooling_system' ? $('#cooling-system-list') :
                    type === 'gpu' ? $('#gpu-list') :
                        type === 'power_supply' ? $('#power-supply-list') :
                            type === 'storage' ? $('#storage-list') :
                                $('#case-list');
    const selectedComponentText = type === 'cpu' ? $('#selected-cpu') :
        type === 'motherboard' ? $('#selected-motherboard') :
            type === 'ram' ? $('#selected-ram') :
                type === 'cooling_system' ? $('#selected-cooling-system') :
                    type === 'gpu' ? $('#selected-gpu') :
                        type === 'power_supply' ? $('#selected-power-supply') :
                            type === 'storage' ? $('#selected-storage') :
                                $('#selected-case');
    listContainer.empty();

    if (components.length === 0) {
        listContainer.append('<p>No compatible items found.</p>');
        return;
    }

    components.forEach((item) => {
        const isActive =
            (type === 'cpu' && item.id === selectedCPU) ||
            (type === 'motherboard' && item.id === selectedMotherboard) ||
            (type === 'ram' && item.id === selectedRAM) ||
            (type === 'cooling_system' && item.id === selectedCoolingSystem) ||
            (type === 'gpu' && item.id === selectedGPU) ||
            (type === 'power_supply' && item.id === selectedPowerSupply) ||
            (type === 'storage' && item.id === selectedStorage) ||
            (type === 'case' && item.id === selectedCase);

        const html = `
            <div class="component-item ${isActive ? 'active' : ''}" data-id="${item.id}" data-type="${type}" data-price="${item.price}">
                <img src="${item.image_url}" alt="${item.name}">
                <h3>${item.name}</h3>
                <p>Price: ${item.price}₴</p>
                
                <div class="component-item-view">
                    <a href="/${type}s/${item.id}/">More details</a>
                </div>
            </div>
        `;
        listContainer.append(html);
    });

    const selectedItem =
        type === 'cpu' ? components.find(item => item.id === selectedCPU) :
            type === 'motherboard' ? components.find(item => item.id === selectedMotherboard) :
                type === 'ram' ? components.find(item => item.id === selectedRAM) :
                    type === 'cooling_system' ? components.find(item => item.id === selectedCoolingSystem) :
                        type === 'gpu' ? components.find(item => item.id === selectedGPU) :
                            type === 'power_supply' ? components.find(item => item.id === selectedPowerSupply) :
                                type === 'storage' ? components.find(item => item.id === selectedStorage) :
                                    components.find(item => item.id === selectedCase);

    selectedComponentText.html(selectedItem ? `${selectedItem.name} - ${selectedItem.price}₴` : 'None');
    updateTotalPrice();
}

function selectComponent(element, type) {
    const id = $(element).data('id');
    const price = parseInt($(element).data('price'));

    // Toggle selection
    if ($(element).hasClass('active')) {
        $(element).removeClass('active');
        if (type === 'cpu') {
            selectedCPU = null;
        } else if (type === 'motherboard') {
            selectedMotherboard = null;
        } else if (type === 'ram') {
            selectedRAM = null;
        } else if (type === 'cooling_system') {
            selectedCoolingSystem = null;
        } else if (type === 'gpu') {
            selectedGPU = null;
        } else if (type === 'power_supply') {
            selectedPowerSupply = null;
        } else if (type === 'storage') {
            selectedStorage = null;
        } else {
            selectedCase = null;
        }

        totalPrice -= price;
    } else {
        $(element).siblings().removeClass('active');
        $(element).addClass('active');
        if (type === 'cpu') {
            selectedCPU = id;
        } else if (type === 'motherboard') {
            selectedMotherboard = id;
        } else if (type === 'ram') {
            selectedRAM = id;
        } else if (type === 'cooling_system') {
            selectedCoolingSystem = id;
        } else if (type === 'gpu') {
            selectedGPU = id;
        } else if (type === 'power_supply') {
            selectedPowerSupply = id;
        } else if (type === 'storage') {
            selectedStorage = id;
        } else {
            selectedCase = id;
        }

        totalPrice += price;
    }

    fetchComponents();
}

function updateTotalPrice() {
    $('#total-price').text(`${totalPrice}₴`);
}

$(document).on('click', '.component-item', function () {
    const type = $(this).data('type');
    selectComponent(this, type);
});

$(document).ready(function () {
    fetchComponents();
});

function saveBuild() {
    const data = {
        cpu: selectedCPU,
        motherboard: selectedMotherboard,
        gpu: selectedGPU,
        ram: selectedRAM,
        storage: selectedStorage,
        cooling_system: selectedCoolingSystem,
        power_supply: selectedPowerSupply,
        case: selectedCase
    };

    $.ajax({
        url: '/save_computer_build/',
        type: 'POST',
        data: data,
        headers: { "X-CSRFToken": getCSRFToken() },
        success: function(response) {
            if (response.status === 'success') {
                alert('Build saved successfully!');
            } else {
                alert('Error: ' + response.message);
            }
        },
        error: function() {
            alert('Failed to save the build. Please try again.');
        }
    });
}

function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
}
