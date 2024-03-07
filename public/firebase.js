
const firebaseConfig = {
  apiKey: "AIzaSyACZ4CyBSFjt-cbDHOWqJx8defhN-FayzA",
  authDomain: "polilisteningtest.firebaseapp.com",
  projectId: "polilisteningtest",
  storageBucket: "polilisteningtest.appspot.com",
  messagingSenderId: "357670630355",
  appId: "1:357670630355:web:ee81659aaca8fff5b4f526",
  measurementId: "G-JRFKQR7PDV"
};
  
// Inizializza l'app Firebase
firebase.initializeApp(firebaseConfig);


  // Test dummy di connessione a Firebase
if (firebase.apps.length === 0) {
    console.error("Modulo Firebase SDK non configurato correttamente!");
  } else {
    // console.log("Connessione a Firebase stabilita correttamente!");
  }

var db = firebase.firestore();

var results = db.collection("Results_Test");



function sendUserDataToFirebase(age, gender, years_training, country, feedback, rhythm, score) {
  
  var userData = {
    age: age,
    gender: gender,
    years_training: years_training,
    country: country,
    feedback: feedback,
  };

  var ratings = [];
  for (var i = 0; i < rhythm.length; i++) {
    var rating = {
      rhythm: rhythm[i],
      score: score[i]
    };
    ratings.push(rating);
  }

  var userRatings = ratings;

  console.log(userData, userRatings);

  // Aggiunta dei dati come documento nella raccolta creata

  results.add({
    userData: userData,
    userRatings: userRatings,
  })
  .then(function(docRef) {
    console.log("Documento aggiunto con ID:", docRef.id);
  })
  .catch(function(error) {
    console.error("Errore nell'aggiunta del documento:", error);
  });


}

