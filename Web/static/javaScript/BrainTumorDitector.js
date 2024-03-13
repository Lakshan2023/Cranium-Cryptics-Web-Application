// this function is used to preview the image
function previewImage() {
    // Get the file input element
    const fileInput = document.getElementById('fileInput');
    // Get the image holder element
    const imageHolder = document.querySelector('.holder');
    // Get the magnifying glass element
    const magnifyingGlass = document.querySelector('.magnifying-glass-effect');
    // Get the span element
    const span = document.querySelector('.span-image');

    // Get the file
    const file = fileInput.files[0];

    // Check if a file is selected
    if (file) {
        // Create a new FileReader
        const reader = new FileReader();
        reader.onload = function (e) {
            // Set the src attribute of the image holder
            imageHolder.src = e.target.result;
            span.style.display = 'none';
            imageHolder.style.display = 'block'; // Make sure image holder is displayed

            // Attach event listeners
            imageHolder.addEventListener('mousemove', function(e) {
                const rect = imageHolder.getBoundingClientRect();
                const mouseX = e.clientX - rect.left;
                const mouseY = e.clientY - rect.top;

                magnifyingGlass.style.backgroundImage = `url('${imageHolder.src}')`;
                magnifyingGlass.style.backgroundPosition = `-${mouseX * 0.95}px -${mouseY * 0.95}px`;
                magnifyingGlass.style.left = `${mouseX - 20}px`;
                magnifyingGlass.style.top = `${mouseY - 10}px`;
            });

            imageHolder.addEventListener('mouseenter', function() {
                magnifyingGlass.style.display = 'block';
                document.body.style.cursor = 'none'; // Hide cursor
            });

            imageHolder.addEventListener('mouseleave', function() {
                magnifyingGlass.style.display = 'none';
                document.body.style.cursor = 'auto'; // Restore cursor
            });

            magnifyingGlass.style.pointerEvents = 'none'; // Allows cursor to pass through magnifying glass
        };

        reader.readAsDataURL(file);
    } else {
        // If no file is selected, show the span element
        span.style.display = 'block';
        imageHolder.style.display = 'none'; // Hide image holder
        imageHolder.src = ''; // Clear src attribute
    }
}



// Ensure the DOM is fully loaded before trying to access elements
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('fileInput');
    fileInput.addEventListener('change', previewImage);
});


document.addEventListener("DOMContentLoaded", function () {
    const dropArea = document.getElementById("dropArea");

    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    // Highlight drop area when a file is dragged over it
    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });

    // Handle dropped files
    dropArea.addEventListener('drop', handleDrop, false);

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    function highlight() {
        dropArea.classList.add('active');
    }

    function unhighlight() {
        dropArea.classList.remove('active');
    }

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;

        handleFiles(files);
    }

    function handleFiles(files) {
        if (files.length > 0) {
            const file = files[0];

            // Check if the dropped file is an image
            if (file.type.startsWith('image/')) {
                // Display the image in the image-holding-section
                const reader = new FileReader();
                reader.onload = function (e) {
                    const img = new Image();
                    img.src = e.target.result;
                    img.alt = 'Dropped Image';
                    document.getElementById('imagePreview').innerHTML = '';
                    document.getElementById('imagePreview').appendChild(img);
                };
                reader.readAsDataURL(file);
            }
        }
    }
});


const tumor_status = document.querySelector('.tumor-status');
const type_status = document.querySelector('.type-status');
const probability_status = document.querySelector('.probability-status');
const probabiliity_status_type = document.querySelector('.probability-status-type');

function displayUpdateTumorStatus(){
    tumor_status.innerHTML = "Status : Not Scanned";
    type_status.innerHTML = "Type : Not Scanned";
    probability_status.innerHTML = "Probability : 0.00";
    probabiliity_status_type.innerHTML = "Probability : 0.00";
}

const alzheimer_status = document.querySelector('.Alzheimer-status');
const alzheimer_probability_status = document.querySelector('.alzheimer-probability');
const  alzheimer_probability_status_type = document.querySelector('.Alzheimer-type');

function displayUpdateAlzheimerStatus(){
    alzheimer_status.innerHTML = "Status : Not Scanned";
    alzheimer_probability_status.innerHTML = "Probability : 0.00";
    alzheimer_probability_status_type.innerHTML = "Detected Type : None";
}

const stroke_status = document.querySelector('.stroke-status');
const stroke_probability_status = document.querySelector('.stroke-probability');

function displayUpdateStrokeStatus(){
     stroke_status.innerHTML = "Status : Not Scanned";
     stroke_probability_status.innerHTML = "Probability : 0.00";
}


const reportTumour = document.querySelector('.report-tumour');
const reportTumourType = document.querySelector('.report-tumour-type');
const reportStroke = document.querySelector('.report-stroke');
const reportAlzheimer = document.querySelector('.report-alzheimer');

function displayUpdateReportStatus(){
    reportTumour.innerHTML = "<h2>Not Scanned</h2>";
    reportTumourType.innerHTML = "<h2>Not Scanned</h2>";
    reportStroke.innerHTML = "<h2>Not Scanned</h2>";
    reportAlzheimer.innerHTML = "<h2>Not Scanned</h2>";

}
function clickScan(event, image_path) {
    event.preventDefault();
    alert(image_path);
    const imagePreview = document.querySelector('.imagePreview');
    if (imagePreview.src !== "") {
        imagePreview.innerHTML = `<img src="${image_path}" alt="Preview" class="holder" /> <div class="magnifying-glass-effect"></div>`;
    }
}

const magnifyingGlass = document.querySelector('.magnifying-glass-effect');
const imageHolder = document.querySelector('.holder');
imageHolder.addEventListener('mousemove', function(e) {
    const rect = imageHolder.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;

    magnifyingGlass.style.backgroundImage = `url('${imageHolder.src}')`;
    magnifyingGlass.style.backgroundPosition = `-${mouseX * 0.95}px -${mouseY * 0.95}px`;
    magnifyingGlass.style.left = `${mouseX - 20}px`;
    magnifyingGlass.style.top = `${mouseY - 10}px`;
});

imageHolder.addEventListener('mouseenter', function() {
    magnifyingGlass.style.display = 'block';
    document.body.style.cursor = 'none'; // Hide cursor
});

imageHolder.addEventListener('mouseleave', function() {
    magnifyingGlass.style.display = 'none';
    document.body.style.cursor = 'auto'; // Restore cursor
});




// Function to show or hide the scanning animation
function toggleScanningAnimation(show) {
    const scanningAnimation = document.querySelector(".scan-box");
    scanningAnimation.style.display = show ? "flex" : "none";
    if(scanningAnimation.style.display === "flex"){
        scanningAnimation.style.justifyContent = "center";
        scanningAnimation.style.alignItems = "center";
    }

}

// Function to handle file input change event
function handleFileInputChange() {
    var fileInput = document.getElementById("fileInput");
    var imagePreview = document.getElementById("imagePreview");

    // Check if a file is selected
    if (fileInput.files.length > 0) {
        // Show scanning animation
        toggleScanningAnimation(true);

    } else {
        // Hide scanning animation
        toggleScanningAnimation(false);
    }
}

// Attach event listener to file input change event
document.querySelector(".scan-button").addEventListener("click", handleFileInputChange);


function disableLink() {
    const reportLink = document.getElementById('reportLink');

    if (reportLink !== null) {
        reportLink.href = "javascript:void(0)";

        reportLink.onclick = null;
    }
}









