// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/12.14.0/firebase-app.js";
import { getAuth, signInWithPopup, GoogleAuthProvider } from "https://www.gstatic.com/firebasejs/12.14.0/firebase-auth.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/12.14.0/firebase-analytics.js";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyALQp0P1qawtSVsBlIXn3-FjSmVRlQpwbY",
  authDomain: "first-project-a9290.firebaseapp.com",
  projectId: "first-project-a9290",
  storageBucket: "first-project-a9290.firebasestorage.app",
  messagingSenderId: "875231585371",
  appId: "1:875231585371:web:bfccc2787650409afc8b7e",
  measurementId: "G-2Y8ZJTEFRG"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const analytics = getAnalytics(app);
const provider = new GoogleAuthProvider();

// Expose Google Sign-In method globally
window.signInWithGoogle = async () => {
  try {
    const result = await signInWithPopup(auth, provider);
    const idToken = await result.user.getIdToken();
    
    // Call the global handleGoogleLogin callback in main.js
    if (window.handleGoogleLogin) {
      await window.handleGoogleLogin({ credential: idToken });
    }
  } catch (error) {
    console.error("Firebase Sign-In Error:", error);
    if (window.showToast) {
      window.showToast(error.message, true);
    }
  }
};
