document.querySelectorAll('.nav-link').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        const targetId = this.getAttribute('href').substring(1);
        const targetElement = document.getElementById(targetId);

        if (targetElement) {
            window.scrollTo({
                top: targetElement.offsetTop - document.querySelector('.header').offsetHeight, // Subtract header height
                behavior: 'smooth'
            });
        }
    });
});
function enableEditing() {
    document.querySelectorAll(".profile-info input").forEach(input => {
        input.removeAttribute("disabled");
    });

    document.getElementById("edit-btn").style.display = "none";
    document.getElementById("save-btn").style.display = "inline-block";
    document.getElementById("cancel-btn").style.display = "inline-block";
    document.getElementById("change-pic-btn").style.display = "inline-block";
}

function cancelChanges() {
    document.querySelectorAll(".profile-info input").forEach(input => {
        input.setAttribute("disabled", "true");
    });

    document.getElementById("edit-btn").style.display = "inline-block";
    document.getElementById("save-btn").style.display = "none";
    document.getElementById("cancel-btn").style.display = "none";
    document.getElementById("change-pic-btn").style.display = "none"; 
}

function saveChanges() {
    alert("Changes Saved!");

    document.querySelectorAll(".profile-info input").forEach(input => {
        input.setAttribute("disabled", "true");
    });

    document.getElementById("edit-btn").style.display = "inline-block";
    document.getElementById("save-btn").style.display = "none";
    document.getElementById("cancel-btn").style.display = "none";
    document.getElementById("change-pic-btn").style.display = "none";
}

function previewImage(event) {
    const reader = new FileReader();
    reader.onload = function() {
        document.getElementById('profile-img').src = reader.result;
    };
    reader.readAsDataURL(event.target.files[0]);
}