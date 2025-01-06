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
            document.querySelectorAll('.navbar button').forEach(button => {
              button.addEventListener('click', () => {
                  const sectionId = button.textContent.trim().toLowerCase().replace(/\s+/g, '-'); // Convert button text to section ID
                  const section = document.querySelector(`#${sectionId}`);
                  if (section) {
                      section.scrollIntoView({ behavior: 'smooth' });
                  }
              });
          });