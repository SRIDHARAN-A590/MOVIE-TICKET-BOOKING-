// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import { getAuth, signInWithPopup, GoogleAuthProvider, signInWithEmailAndPassword, createUserWithEmailAndPassword, signOut } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-auth.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-analytics.js";
import { getFirestore, collection, doc, getDocs, getDoc, setDoc, addDoc, updateDoc, deleteDoc, query, where, arrayUnion, arrayRemove } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-firestore.js";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_AUTH_DOMAIN",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_STORAGE_BUCKET",
  messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
  appId: "YOUR_APP_ID",
  measurementId: "YOUR_MEASUREMENT_ID"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);
const analytics = getAnalytics(app);
const provider = new GoogleAuthProvider();

// Expose Firebase tools globally so api.js can use them
window.firebaseAuth = auth;
window.firebaseDb = db;
window.firebaseSignInWithPopup = signInWithPopup;
window.firebaseGoogleProvider = provider;
window.firebaseSignInWithEmailAndPassword = signInWithEmailAndPassword;
window.firebaseCreateUserWithEmailAndPassword = createUserWithEmailAndPassword;
window.firebaseSignOut = signOut;

// Export Firestore methods to window so we don't have to rewrite imports everywhere
window.fsCollection = collection;
window.fsDoc = doc;
window.fsGetDocs = getDocs;
window.fsGetDoc = getDoc;
window.fsSetDoc = setDoc;
window.fsAddDoc = addDoc;
window.fsUpdateDoc = updateDoc;
window.fsDeleteDoc = deleteDoc;
window.fsQuery = query;
window.fsWhere = where;
window.fsArrayUnion = arrayUnion;
window.fsArrayRemove = arrayRemove;

// Expose Google Sign-In method globally
window.signInWithGoogle = async () => {
  try {
    const result = await signInWithPopup(auth, provider);
    
    // Set user data locally
    const user = {
        uid: result.user.uid,
        name: result.user.displayName,
        email: result.user.email,
        role: result.user.email === 'admin@movie.com' ? 'admin' : 'user' // Simple admin check
    };
    localStorage.setItem('user', JSON.stringify(user));
    localStorage.setItem('token', result.user.accessToken);

    if (window.handleGoogleLogin) {
      await window.handleGoogleLogin(result);
    }
  } catch (error) {
    console.error("Firebase Sign-In Error:", error);
    if (window.showToast) {
      window.showToast(error.message, true);
    }
  }
};
