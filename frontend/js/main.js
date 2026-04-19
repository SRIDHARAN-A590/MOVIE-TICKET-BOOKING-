// Global Utilities
function showToast(message, isError = false) {
    const toast = document.getElementById('toast');
    if (!toast) return;
    
    toast.textContent = message;
    toast.style.backgroundColor = isError ? 'var(--seat-booked)' : 'var(--seat-available)';
    toast.className = "show";
    setTimeout(() => { toast.className = toast.className.replace("show", ""); }, 3000);
}

// Global Google Login Callback
window.handleGoogleLogin = async (response) => {
    try {
        showLoader();
        const res = await Api.handleGoogleLogin(response.credential);
        Api.setToken(res.token, res.user);
        showToast('Google Login Successful!', false);
        
        if (res.user.role === 'admin') window.location.href = 'admin-dashboard.html';
        else window.location.href = 'index.html';
    } catch (err) {
        showToast(err.message, true);
    } finally {
        hideLoader();
    }
};

function showLoader() {
    const loader = document.getElementById('loader');
    if (loader) loader.style.display = 'block';
}

function hideLoader() {
    const loader = document.getElementById('loader');
    if (loader) loader.style.display = 'none';
}

function renderNavbar() {
    const navRight = document.querySelector('.nav-right');
    if (!navRight) return;
    
    if (Api.isLoggedIn()) {
        const user = JSON.parse(localStorage.getItem('user'));
        navRight.innerHTML = `
            <span style="margin-right: 15px;">Hi, ${user.name}</span>
            <a href="history.html" class="btn btn-outline" style="margin-right: 15px;">History</a>
            <button onclick="Api.logout()" class="btn btn-primary">Logout</button>
        `;
    } else {
        navRight.innerHTML = `
            <a href="login.html" class="btn btn-outline" style="margin-right: 15px;">Login</a>
            <a href="register.html" class="btn btn-primary">Register</a>
        `;
    }
}

// Format date securely
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

document.addEventListener('DOMContentLoaded', () => {
    // Add generic navbar logic securely without overwriting the whole document dynamically if not needed
    renderNavbar();
});
