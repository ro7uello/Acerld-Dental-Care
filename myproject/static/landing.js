
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
          const dentists = document.querySelectorAll('.dentist');
          const dentistPopup = document.getElementById('dentist-popup');
          const dentistPopupImage = document.getElementById('dentist-popup-image');
          const dentistPopupText = document.getElementById('dentist-popup-text');
  
          const dentistData = {
            dr_peter: {
                image: dentistImages.dr_peter,
                description: 
                  `<p>A graduate of doctor of dental medicine in Our Lady of Fatima University in 2003. </p>
                
                <p>She was awarded as the “scholar of the year” for winning a dental interschool competition given by the Southern California Filipino Dental Society held in Philippine Dental Association Annual convention in 2002. </p>
                
                <p>In 2004-2011, she became part of Spectrumed Incorporated  as sales manager to division head of dental department. </p>
                
                <p>In 2004 she has given the chance to pursue her studies in Oral Implantology from International Research and Development Institute, Tel-aviv, Israel</p>
                
                <p>In 2006-2007, she completed her post-graduate course of Oral Implantology in International Center for Dental Education Research and Development Institute, Alpha-Bio, Philippines. </p>
                
                <p>In 2008-2009, she further studied a post-graduate preceptorship in dental implantology under Nobel Biocare, Philippines. </p>
                
                <p>In 2009, she was sponsored a  training in GUIDED IMPLANT Surgery using Nobel Guide under Dr. Jasmes Chow in Hong Kong. </p>
                <p>In the same year 2009, she was recognized as the EMPLOYEE OF THE YEAR by SPECTRUMED Inc. </p>
                
                <p>In 2011-2014, she migrated to Singapore as Clinical Sales Executive of Nobel Biocare and has awarded as Top Sales Silver Awardee in Southeast Asia in 2013. </p>
                
                <p>In 2015-2019, she has  worked with 2 companies as Business Development Manager in Apexmed  and Clinical consultant in Spectrumed</p>
                
                <p>In 2015, she studied a preceptorship in Orthodontics under Dr. Enrico Dolatre. </p>
                
                <p>In 2016, she has achieved her official license of Photon Induced Photoaccoustic Streaming Technology (Dental L:aser)  given by Laser and Health in Slovenia, Europe. </p>
                
                <p>In 2016-2018, she completed her post-graduate course in Biofunctional Dentistry which involves teeth-muscles and TMJ. </p>
                
                <p>Last year, she started  studying Orofacial pain and Occlusion under Dr. Elaine Rozul, who studied in University of Louisiana and Dawson Academy in USA. </p>
                
                <p>Currently, practicing in Acerld Dental Care as the owner and an active member of Philippine Academy of Implant Dentistry and Philippine College of Oral Implantologist.-Dr. Peter Lou Santiago-Caronan</p>`
            },
          
        };
  
          dentists.forEach(dentist => {
              dentist.addEventListener('click', () => {
                  const dentistKey = dentist.dataset.dentist;
                  const data = dentistData[dentistKey];
  
                  if (data) {
                      dentistPopupImage.src = data.image;
                      dentistPopupText.innerHTML = data.description;
                      dentistPopup.classList.add('show');
                  }
              });
          });
  
          function closeDentistPopup() {
              dentistPopup.classList.remove('show');
          }
  
          dentistPopup.addEventListener('click', function(event) {
              if (event.target === dentistPopup) {
                  closeDentistPopup();
              }
          });

const serviceImages = document.querySelectorAll('.service-image');
const popup = document.getElementById('popup');
const popupContent = document.querySelector('.popup-content');

const serviceData = {
    surgery: `
        <table>
            <thead>
                <tr>
                    <th>Service</th>
                    <th>Price</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Gingival Contouring</td>
                    <td>₱5,000</td>
                </tr>
                <tr>
                    <td>Perio Surgery</td>
                    <td>₱7,500</td>
                </tr>
                <tr>
                    <td>Impacted tooth removal</td>
                    <td>₱10,000</td>
                </tr>
                <tr>
                    <td>Dental Implant without a crown</td>
                    <td>₱100,000</td>
                </tr>
            </tbody>
        </table>
    `,
    denture: `
    <h4>Laminates/Veeners</h4>
        <table>
            <thead>
                <tr>
                    <th>Service</th>
                    <th>Price</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Direct Composite</td>
                    <td>₱5,000</td>
                </tr>
                <tr>
                    <td>Indirect Composite</td>
                    <td>₱10,000</td>
                </tr>
                <tr>
                    <td>E-max</td>
                    <td>₱15,000</td>
                </tr>
                <tr>
                    <td>Zirconia</td>
                    <td>₱20,000</td>
                </tr>
            </tbody>
        </table>
    `,
    crown: `
        <h4>Porcelain fused to metal</h4>
        <table>
            <thead>
                <tr>
                    <th>Service</th>
                    <th>Price</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Ordinary metal</td>
                    <td>₱10,000</td>
                </tr>
                <tr>
                    <td>Tilite Metal</td>
                    <td>₱15,000</td>
                </tr>
            </tbody>
        </table>

        <h4>Pure Ceramic Crown</h4>
        <table>
            <thead>
                <tr>
                    <th>Service</th>
                    <th>Price</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Alumina</td>
                    <td>₱17,000</td>
                </tr>
                <tr>
                    <td>E-max</td>
                    <td>₱20,000</td>
                </tr>
                <tr>
                    <td>Zirconia</td>
                    <td>₱25,000</td>
                </tr>
            </tbody>
        </table>
    `,
    removable: `
        <h4>Unilateral</h4>
        <table>
            <thead>
                <tr>
                    <th>Service</th>
                    <th>Price</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Acrylic</td>
                    <td>₱15,000</td>
                </tr>
                <tr>
                    <td>Flexible(bounded teeth only)</td>
                    <td>₱20,000</td>
                </tr>
            </tbody>
        </table>

        <h4>Bilateral</h4>
        <table>
            <thead>
                <tr>
                    <th>Service</th>
                    <th>Price</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Acrylic</td>
                    <td>₱20,000</td>
                </tr>
                <tr>
                    <td>Flexible(bounded teeth only)</td>
                    <td>₱25,000</td>
                </tr>
            </tbody>
        </table>
    `,
    complete: `
        <table>
            <thead>
                <tr>
                    <th>Service</th>
                    <th>Price</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Acrylic</td>
                    <td>₱20,000</td>
                </tr>
                <tr>
                    <td>Thermosens/Ivocap</td>
                    <td>₱25,000</td>
                </tr>
                <tr>
                    <td>Biofunctional Prosthetic System</td>
                    <td>₱40,000</td>
                </tr>
            </tbody>
        </table>
     `,
    others: `
        <table>
            <thead>
                <tr>
                    <th>Service</th>
                    <th>Price</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Consultation</td>
                    <td>₱1,000</td>
                </tr>
                <tr>
                    <td>Cleaning</td>
                    <td>₱1,000</td>
                </tr>
                <tr>
                    <td>Flouride Varnish Application</td>
                    <td>₱1,500</td>
                </tr>
                <tr>
                    <td>Composite Restoration(per surface)</td>
                    <td>₱1,000</td>
                </tr>
                <tr>
                    <td>Extraction</td>
                    <td>₱1,000</td>
                </tr>
                <tr>
                    <td>Xray/panoramic xray/cbct scan</td>
                    <td>₱650/₱1,000/₱6,000</td>
                </tr>
                <tr>
                    <td>Teeth Whitening</td>
                    <td>₱15,000</td>
                </tr>
                <tr>
                    <td>Orthodontic Appliance (Braces)</td>
                    <td>₱50,000</td>
                </tr>
                <tr>
                    <td>Root Canal Therapy</td>
                    <td>₱10,000</td>
                </tr>
                <tr>
                    <td>Post and Core</td>
                    <td>₱5,000</td>
                </tr>
                <tr>
                    <td>Bite Analysis</td>
                    <td>₱5,000</td>
                </tr>
            </tbody>
        </table>
    `,
};

serviceImages.forEach(image => {
    image.addEventListener('click', () => {
        const serviceType = image.dataset.service;
        popupContent.innerHTML = serviceData[serviceType] || "<p>Content coming soon...</p>"; // Default content
        popup.style.display = 'block';
        popup.classList.add('show'); 
    });
});

function closePopup() {
  popup.classList.remove('show');
 
  setTimeout(() => {
    popup.style.display = 'none';
  }, 300); 
}

popup.addEventListener('click', function(event) {
  if (event.target === popup) {
    closePopup();
  }
});
