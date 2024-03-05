const firebaseConfig = {
    apiKey: "AIzaSyChuCsLIaZDj4nfI1jE9Dpbkt2CFZSKR1c",
    authDomain: "craniumcryptics.firebaseapp.com",
    databaseURL: "https://craniumcryptics-default-rtdb.firebaseio.com",
    projectId: "craniumcryptics",
    storageBucket: "craniumcryptics.appspot.com",
    messagingSenderId: "415799673124",
    appId: "1:415799673124:web:31e4bf310fda12df4c73b1"
  };

firebase.initializeApp(firebaseConfig);

const getElementVal = (id) => {
  return document.getElementById(id).value;
};

var hForm = firebase.database().ref('UserData')

document.getElementById("loginForm").addEventListener('submit', submitLoginForm);

function submitLoginForm(e) {
    e.preventDefault();

    var loginUsername = getElementVal('login__username');
    var loginPassword = getElementVal('login__password');

    viewData(loginUsername, loginPassword)

}

const viewData = (loginUsername, loginPassword) => {

hForm.child(loginUsername).once('value', function(snapshot) {
        const userData = snapshot.val();
        if (userData) {
            const storedPassword = userData.password;
            const storedEmail = userData.email;
            if (loginPassword === storedPassword) {
              displayAlert("Login Successfull")
              getData(loginUsername);

              setTimeout(() => {
                window.location.href = '/Dashboard';
            }, 1000);

            } else {
              displayAlert("Incorrect password")
            }
          } else {
            displayAlert("User not Found")
          }
  });

  // Customized alert messages
function displayAlert(message) {
  var issue = document.getElementById("customAlert");
  var alertMessage = document.getElementById("alertMessage");
  alertMessage.innerHTML = message;
  issue.style.display = "block";


  //Closes the alert popup when anywhere in the screen is clicked
  window.onclick = function(event) {
    if (event.target == issue) {
      issue.style.display = "none";
    }
  }

}
}

function getData(userName) {
    const user_ref = firebase.database().ref('UserData/' + userName); // Use the userName parameter
    user_ref.once('value', (snapshot) => {
        const data = snapshot.val();
        if (data) {
            // Create a data object containing the user data
            const userData = {
                userName: data.userName,
                password: data.password,
                email : data.email,
            };

            // Convert the data object to JSON format
            const jsonData = JSON.stringify(userData);

            // Store the JSON data in local storage
            localStorage.setItem('userData', jsonData);


        } else {
            console.error("User data not found");
        }
    });
}

function createUserCollection(user){
    firebase.firestore().collection("users").
    doc(user.userName).set({
        userName: user.userName,
        email: user.email,
        password: user.password,
    })
}

async function getUserData(userName){
    const user = await firebase.firestore().collection("users").doc(userName).get();
    return user.data();
}


