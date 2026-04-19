const API_URL = 'http://localhost:5000/api';

class Api {
    static getToken() {
        return localStorage.getItem('token');
    }

    static setToken(token, user) {
        localStorage.setItem('token', token);
        localStorage.setItem('user', JSON.stringify(user));
    }

    static async handleGoogleLogin(credential) {
        const response = await fetch(`${API_URL}/auth/google`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ credential })
        });
        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.message || 'Google Auth failed');
        }
        return response.json();
    }

    static logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = 'login.html';
    }

    static isLoggedIn() {
        return !!this.getToken();
    }

    static async request(endpoint, method = 'GET', data = null) {
        const headers = {
            'Content-Type': 'application/json'
        };

        const token = this.getToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const config = {
            method,
            headers
        };

        if (data) {
            config.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(`${API_URL}${endpoint}`, config);
            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.message || 'Something went wrong');
            }
            
            return result;
        } catch (error) {
            throw error;
        }
    }

    static async login(email, password) {
        return this.request('/auth/login', 'POST', { email, password });
    }

    static async register(name, email, password) {
        return this.request('/auth/register', 'POST', { name, email, password });
    }

    static async getMovies() {
        return this.request('/movies');
    }

    static async getMovieDetails(id) {
        return this.request(`/movies/${id}`);
    }

    static async getMovieShows(id) {
        return this.request(`/movies/${id}/shows`);
    }

    static async getShowSeats(id) {
        return this.request(`/shows/${id}/seats`);
    }

    static async createBooking(showId, seatIds) {
        return this.request('/bookings', 'POST', { show_id: showId, seat_ids: seatIds });
    }

    static async makePayment(bookingId, amount, method) {
        return this.request('/payments', 'POST', { booking_id: bookingId, amount, payment_method: method });
    }

    static async getHistory() {
        return this.request('/user/history');
    }

    static async cancelBooking(id) {
        return this.request(`/bookings/${id}/cancel`, 'POST');
    }
}
