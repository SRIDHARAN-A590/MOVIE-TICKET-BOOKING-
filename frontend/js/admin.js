// Admin API handling
const AdminApi = {
    async getStats() {
        return Api.request('/admin/stats');
    },
    async getMovies() {
        return Api.request('/movies');
    },
    async addMovie(data) {
        return Api.request('/admin/movies', 'POST', data);
    },
    async updateMovie(id, data) {
        return Api.request(`/admin/movies/${id}`, 'PUT', data);
    },
    async deleteMovie(id) {
        return Api.request(`/admin/movies/${id}`, 'DELETE');
    },
    async getTheatres() {
        return Api.request('/admin/theatres');
    },
    async addTheatre(data) {
        return Api.request('/admin/theatres', 'POST', data);
    },
    async deleteTheatre(id) {
        return Api.request(`/admin/theatres/${id}`, 'DELETE');
    },
    async getShows() {
        return Api.request('/admin/shows');
    },
    async addShow(data) {
        return Api.request('/admin/shows', 'POST', data);
    },
    async updateShow(id, data) {
        return Api.request(`/admin/shows/${id}`, 'PUT', data);
    },
    async deleteShow(id) {
        return Api.request(`/admin/shows/${id}`, 'DELETE');
    },
    async getBookings() {
        return Api.request('/admin/bookings');
    },
    async cancelBooking(id) {
        return Api.request(`/admin/bookings/${id}`, 'DELETE');
    },
    async getUsers() {
        return Api.request('/admin/users');
    }
};

// UI Helpers for Admin
function openModal(id) {
    document.getElementById(id).classList.add('show');
}

function closeModal(id) {
    document.getElementById(id).classList.remove('show');
}
