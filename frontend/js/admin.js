// Admin API handling
const AdminApi = {
    async getStats() {
        const moviesSnap = await window.fsGetDocs(window.fsCollection(window.firebaseDb, 'movies'));
        const theatresSnap = await window.fsGetDocs(window.fsCollection(window.firebaseDb, 'theatres'));
        const showsSnap = await window.fsGetDocs(window.fsCollection(window.firebaseDb, 'shows'));
        const usersSnap = await window.fsGetDocs(window.fsCollection(window.firebaseDb, 'users'));
        const bookingsSnap = await window.fsGetDocs(window.fsCollection(window.firebaseDb, 'bookings'));
        
        return {
            movies: moviesSnap.size,
            theatres: theatresSnap.size,
            shows: showsSnap.size,
            users: usersSnap.size,
            bookings: bookingsSnap.size
        };
    },
    async getMovies() {
        return Api.getMovies();
    },
    async addMovie(data) {
        const docRef = await window.fsAddDoc(window.fsCollection(window.firebaseDb, 'movies'), data);
        return { id: docRef.id, ...data };
    },
    async updateMovie(id, data) {
        await window.fsUpdateDoc(window.fsDoc(window.firebaseDb, 'movies', id), data);
        return { id, ...data };
    },
    async deleteMovie(id) {
        await window.fsDeleteDoc(window.fsDoc(window.firebaseDb, 'movies', id));
        return { success: true };
    },
    async getTheatres() {
        const snap = await window.fsGetDocs(window.fsCollection(window.firebaseDb, 'theatres'));
        return snap.docs.map(doc => ({ id: doc.id, ...doc.data() }));
    },
    async addTheatre(data) {
        const docRef = await window.fsAddDoc(window.fsCollection(window.firebaseDb, 'theatres'), data);
        return { id: docRef.id, ...data };
    },
    async deleteTheatre(id) {
        await window.fsDeleteDoc(window.fsDoc(window.firebaseDb, 'theatres', id));
        return { success: true };
    },
    async getShows() {
        const snap = await window.fsGetDocs(window.fsCollection(window.firebaseDb, 'shows'));
        return snap.docs.map(doc => ({ id: doc.id, ...doc.data() }));
    },
    async addShow(data) {
        const docRef = await window.fsAddDoc(window.fsCollection(window.firebaseDb, 'shows'), data);
        return { id: docRef.id, ...data };
    },
    async updateShow(id, data) {
        await window.fsUpdateDoc(window.fsDoc(window.firebaseDb, 'shows', id), data);
        return { id, ...data };
    },
    async deleteShow(id) {
        await window.fsDeleteDoc(window.fsDoc(window.firebaseDb, 'shows', id));
        return { success: true };
    },
    async getBookings() {
        const snap = await window.fsGetDocs(window.fsCollection(window.firebaseDb, 'bookings'));
        return snap.docs.map(doc => ({ id: doc.id, ...doc.data() }));
    },
    async cancelBooking(id) {
        return Api.cancelBooking(id);
    },
    async getUsers() {
        const snap = await window.fsGetDocs(window.fsCollection(window.firebaseDb, 'users'));
        return snap.docs.map(doc => ({ id: doc.id, ...doc.data() }));
    }
};

// UI Helpers for Admin
function openModal(id) {
    document.getElementById(id).classList.add('show');
}

function closeModal(id) {
    document.getElementById(id).classList.remove('show');
}
