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
        var userData = snapshot.val();
        if (userData) {
            var storedPassword = userData.password;
            if (loginPassword === storedPassword) {
              window.location.href = '/Dashboard'
              console.log("Login successful");
              
            } else {
              console.log("Incorrect password");
              alert("Incorrect password")
            }
          } else {
            console.log("User not found");
            alert("User not Found")
          }
    });

}

if(typeof (global) === "undefined") {
    throw new Error("window is undefined");
}

(function(global) {
    var _hash = "!";

    var noBackPlease = function () {
        global.location.href += "#";

        // Making sure we have the fruit available for juice (^__^)
        global.setTimeout(function () {
            global.location.href += "!";
        }, 50);
    };

    global.onhashchange = function () {
        if (global.location.hash !== _hash) {
            global.location.hash = _hash;
        }
    };

    global.onload = function () {
        noBackPlease();
        // Disables backspace on page except on input fields and textarea.
        document.body.onkeydown = function (e) {
            var elm = e.target.nodeName.toLowerCase();
            if (e.which === 8 && (elm !== 'input' && elm !== 'textarea')) {
                e.preventDefault();
            }
            // Stopping the event bubbling up the DOM tree...
            e.stopPropagation();
        };
    };
})(window);

window.addEventListener('load', function() {
        // Disable touchmove event to prevent swipe navigation
        window.addEventListener('touchmove', function(e) {
            e.preventDefault();
        }, { passive: false });
});
