// Function to handle file input change event
function handleFileInputChange(event) {
    const file = event.target.files[0]; // Get the selected file
    if (file) {
        // Create a FileReader object
        const reader = new FileReader();
        reader.onload = function(e) {
            // Set the src attribute of the preview image to the data URL
            document.getElementById('previewImage').src = e.target.result;
        }
        // Read the file as a data URL (base64 encoded)
        reader.readAsDataURL(file);
    }
}

// Add event listener for file input change
document.getElementById('uploadInput').addEventListener('change', handleFileInputChange);

function clearFileInput() {
    updateUserName.innerHTML = userData.userName;
    const userControl = document.querySelector('.user-control');
    const emailControl = document.querySelector('.email-control');
    const passwordControl = document.querySelector('.password-control');
    const confirmPasswordControl = document.querySelector('.confirm-password-control');

    userControl.value = userData.userName;
    emailControl.value = userData.email;
    passwordControl.value = userData.confirmPassword;
    confirmPasswordControl.value = userData.confirmPassword;
}