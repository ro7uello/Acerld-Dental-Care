const appointmentForm = document.getElementById('appointmentForm');
const successMessage = document.getElementById('successMessage');
const otherOptions = document.getElementById('otherOptions');
const materialOptions = document.getElementById('materialOptions');

appointmentForm.addEventListener('submit', function (event) {
    event.preventDefault();
    successMessage.style.display = 'block';
    appointmentForm.reset();
    updateOptions();
    materialOptions.style.display = 'none'; // Hide material options on form reset
});

function updateOptions() {
    const serviceSelect = document.getElementById('service');
    const otherTypeSelect = document.getElementById('otherType');

    otherOptions.style.display = 'none';
    otherTypeSelect.innerHTML = "";
    materialOptions.style.display = 'none'; // Hide material options when changing service

    if (serviceSelect.value === "") {
        return;
    }

    const selectedService = serviceSelect.value;
    let options = [];

    switch (selectedService) {
        case 'other':
            options = ["Consultation", "Cleaning", "Flouride Varnish Application", "Composite Restoration (per surface)", "Extraction", "Xray/Pano/Cbct Scan", "Teeth Whitening", "Orthodontic Appliance (Braces)", "Root Canal Therapy", "Post And Core", "Bite Analysis"];
            break;
        case 'surgery':
            options = ["Dental Implant without a crown", "Impacted Tooth Removal", "Perio Surgery", "Gingival Contouring"];
            break;
        case 'fixed':
            options = ["Direct Composite", "Indirect Composite", "E-max", "Zirconia"];
            break;
        case 'crown':
            options = ["Porcelain fused to metal", "Pure ceramic crown"];
            break;
        case 'removable':
            options = ["Unilateral", "Bilateral"];
            break;
        case 'complete':
            options = ["Acrylic", "Thermosens/Ivocap", "Biofunctional Prosthetic System"];
            break;
        default:
            return;
    }

    otherOptions.style.display = 'block';
    populateOptions(otherTypeSelect, options);
}

function updateMaterialOptions() {
    const otherTypeSelect = document.getElementById('otherType');
    const materialTypeSelect = document.getElementById('materialType');

    materialOptions.style.display = 'none'; // Hide material options initially
    materialTypeSelect.innerHTML = "";

    if (otherTypeSelect.value === "") {
        return;
    }

    let materialTypes = [];

    switch (otherTypeSelect.value) {
        case "Porcelain fused to metal":
            materialTypes = ["Ordinary Metal", "Tilite Metal"];
            break;
        case "Pure ceramic crown":
            materialTypes = ["Alumina", "E-max", "Zirconia"];
            break;
        case "Unilateral":
        case "Bilateral":
            materialTypes = ["Acrylic", "Flexible(bounded teeth only)"];
            break;
        default:
            return;
    }

    materialOptions.style.display = 'block';
    populateOptions(materialTypeSelect, materialTypes);
}

function populateOptions(selectElement, optionsArray) {
    selectElement.innerHTML = "<option value=''>Select an option</option>"; // Add a default option
    optionsArray.forEach(type => {
        const option = document.createElement('option');
        option.value = type;
        option.text = type;
        selectElement.add(option);
    });
}

// Event listeners
document.getElementById('service').addEventListener('change', updateOptions);
document.getElementById('otherType').addEventListener('change', updateMaterialOptions);

// Ensure it updates on page load
window.addEventListener('DOMContentLoaded', () => {
    updateOptions();
    materialOptions.style.display = 'none'; // Hide material options on page load
});