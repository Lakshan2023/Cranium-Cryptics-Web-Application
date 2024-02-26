
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

document.getElementById("regForm").addEventListener('submit', submitForm)

function submitForm(e){
e.preventDefault();

var email = getElementVal('reg_email')
var userName = getElementVal('reg_username')
var password = getElementVal('reg_password')
var confirmPassword = getElementVal('reg_confirm')

saveMessages(email,userName,password,confirmPassword)
}



const saveMessages = (email, userName, password, confirmPassword) => {
var newhForm = hForm.child(userName);

newhForm.set({
  email : email,
  userName : userName,
  password : password,
  confirmPassword : confirmPassword,

  })

};

