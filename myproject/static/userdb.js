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

document.addEventListener('DOMContentLoaded', function() {
    const reviewForm = document.getElementById('review-form');

    reviewForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const reviewText = document.getElementById('review-text').value;

        console.log('Submitting review:', reviewText);  // Debugging line

        fetch('/add-review/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({
                review_text: reviewText
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Response:', data);  // Debugging line
            if (data.status === 'success') {
                alert('Review submitted successfully');
                reviewForm.reset();
            } else {
                alert('Failed to submit review');
            }
        })
        .catch(error => {
            console.error('Error submitting review:', error);
        });
    });
});

let slideIndex = 0;
        
            function showSlides() {
              let slides = document.getElementsByClassName("slides");
              let dots = document.getElementsByClassName("dot");
        
              for (let i = 0; i < slides.length; i++) {
                slides[i].style.display = "none";
              }
                
              slideIndex++;
              if (slideIndex > slides.length) {
                slideIndex = 1;
              }
        
              slides[slideIndex - 1].style.display = "block";
        
              for (let i = 0; i < dots.length; i++) {
                dots[i].classList.remove("active");
              }
        
              dots[slideIndex - 1].classList.add("active");
              setTimeout(showSlides, 3000);
            }
        
            showSlides();
        
            function currentSlide(n) {
              slideIndex = n - 1;
              showSlides();
            }