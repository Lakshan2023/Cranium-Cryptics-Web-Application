let pop = document.querySelector(".profile-popup");

function toggleMenu() {
    const menuContainer = document.querySelector('.menu-container');
    const leftPane = document.querySelector('.left-pane');
    const mainMenu = document.querySelector('.main-menu');
    const menuButton = document.querySelector('.menu-button');
    const menuBurger = document.querySelector('.menu-burger');
    const diseaseCard = document.querySelector('.image-detection-cards');
    const card1 = document.querySelector('.card-1');
    const card2 = document.querySelector('.card-2');
    const card3 = document.querySelector('.card-3');

    if (menuContainer.style.display === 'none' || menuContainer.style.display === '') {
        menuContainer.style.display = 'block';
        leftPane.style.width = '250px';
        mainMenu.style.display = 'block';
        menuButton.display = 'flex';
        menuButton.flexDirection = 'column';
        menuBurger.style.margin_right = '20px';
        menuBurger.innerHTML = '&times;';
        menuBurger.style.fontSize = '35px';
        menuBurger.style.paddig_right = '20px';
        leftPane.style.Color= "#FFF";

    } else {
        menuContainer.style.display = 'none';
        leftPane.style.width = '40px';
        mainMenu.style.display = 'none';
        menuBurger.innerHTML = '&#9776;';
        menuBurger.style.padding_right = '0px';
        menuBurger.style.fontSize = '30px';
        menuBurger.classList.remove('rotate');
        leftPane.style.Color = "#000";
    }

}


const updateUserName = document.querySelector('.user-name');

const storedData = localStorage.getItem('userData');
const userData = JSON.parse(storedData);
usersData= JSON.stringify(userData)

updateUserName.innerHTML = userData.userName;

const userControl = document.querySelector('.user-control');
const emailControl = document.querySelector('.email-control');
const passwordControl = document.querySelector('.password-control');
const confirmPasswordControl = document.querySelector('.confirm-password-control');

if(userControl !== null){
    userControl.value = userData.userName;
    emailControl.value = userData.email;
    passwordControl.value = userData.password;
    confirmPasswordControl.value = userData.password;
}



const previewImageElement = document.querySelector("#previewImage");

// if (previewImageSrc.includes("/static/images/profile.jpeg")) {
//     const profileImage = document.querySelector('.profile-image');
//     profileImage.src = "./static/images/profile.jpeg";
// } else {
    const firebaseConfig = {
          apiKey: "AIzaSyChuCsLIaZDj4nfI1jE9Dpbkt2CFZSKR1c",
          authDomain: "craniumcryptics.firebaseapp.com",
          databaseURL: "https://craniumcryptics-default-rtdb.firebaseio.com",
          projectId: "craniumcryptics",
          storageBucket: "craniumcryptics.appspot.com",
          messagingSenderId: "415799673124",
          appId: "1:415799673124:web:31e4bf310fda12df4c73b1"
  };

  // Initialize Firebase if it's not already initialized
  if (!firebase.apps.length) {
    firebase.initializeApp(firebaseConfig);
  }

    let storageRef = firebase.storage().ref('ProfileImages/' + userData.userName);
    if(storageRef !== null){
    storageRef.getDownloadURL().then((url) => {
        const profileImage = document.querySelector('.profile-image');
        profileImage.src = url;
    }).catch((error) => {
        console.log('Error getting download URL:', error);
    });
}


function ProfilePopView(){
   pop.style.display = "flex";
}

function removeProfileView(){
    pop.style.display = "none"; 
}

document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('fileInput');
    const imageDisplay = document.getElementById('imageDisplay');

    fileInput.addEventListener('change', function (event) {
        const file = event.target.files[0];

        if (file) {
            const reader = new FileReader();

            reader.onload = function (e) {
                imageDisplay.src = e.target.result;
            };

            reader.readAsDataURL(file);
        }
    });
});

function redirectTumour() {
    window.location.href = "BrainTumourDetector.html";
}

function redirectStroke() {
    window.location.href = "BrainStrokeDetector.html";
}

function redirectAlzhimer() {
    window.location.href = "AlzheimerDiseaseDetector.html";
}

function nav_highliter() {
    let current_button = document.querySelector(".current_page");
    if (current_button !== null) {
        current_button.style.transition = "box-shadow 0.5s ease"; // Smooth transition
        current_button.style.boxShadow = "none"; // Remove box shadow
    }
}


function nav_back_highliter() {
    let current_button = document.querySelector(".current_page");
    current_button.style.boxShadow = "0 0 15px rgba(100, 100, 100, 0.60)"
}

function logout() {
    localStorage.removeItem('userData');
}






