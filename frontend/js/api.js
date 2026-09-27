class Api {
    static getToken() {
        return localStorage.getItem('token');
    }

    static setToken(token, user) {
        localStorage.setItem('token', token);
        localStorage.setItem('user', JSON.stringify(user));
    }

    static async handleGoogleLogin(result) {
        return { token: result.user.accessToken, user: JSON.parse(localStorage.getItem('user')) };
    }

    static async logout() {
        await window.firebaseSignOut(window.firebaseAuth);
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = 'login.html';
    }

    static isLoggedIn() {
        return !!this.getToken();
    }

    static async login(email, password) {
        const result = await window.firebaseSignInWithEmailAndPassword(window.firebaseAuth, email, password);
        const user = {
            uid: result.user.uid,
            name: result.user.displayName || email.split('@')[0],
            email: result.user.email,
            role: result.user.email === 'admin@movie.com' ? 'admin' : 'user'
        };
        this.setToken(result.user.accessToken, user);
        return { token: result.user.accessToken, user };
    }

    static async register(name, email, password) {
        const result = await window.firebaseCreateUserWithEmailAndPassword(window.firebaseAuth, email, password);
        const user = {
            uid: result.user.uid,
            name: name,
            email: result.user.email,
            role: result.user.email === 'admin@movie.com' ? 'admin' : 'user'
        };
        // Save user to firestore
        await window.fsSetDoc(window.fsDoc(window.firebaseDb, 'users', result.user.uid), user);
        this.setToken(result.user.accessToken, user);
        return { token: result.user.accessToken, user };
    }

    static async getMovies() {
        const q = window.fsQuery(window.fsCollection(window.firebaseDb, 'movies'));
        const querySnapshot = await window.fsGetDocs(q);
        return querySnapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
    }

    static async getMovieDetails(id) {
        const docRef = window.fsDoc(window.firebaseDb, 'movies', id);
        const docSnap = await window.fsGetDoc(docRef);
        if (docSnap.exists()) {
            return { id: docSnap.id, ...docSnap.data() };
        } else {
            throw new Error("Movie not found");
        }
    }

    static async getMovieShows(id) {
        const q = window.fsQuery(window.fsCollection(window.firebaseDb, 'shows'), window.fsWhere('movie_id', '==', id));
        const querySnapshot = await window.fsGetDocs(q);
        return querySnapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
    }

    static async getShowSeats(id) {
        const docRef = window.fsDoc(window.firebaseDb, 'shows', id);
        const docSnap = await window.fsGetDoc(docRef);
        if (docSnap.exists()) {
            return { booked_seats: docSnap.data().booked_seats || [] };
        } else {
            return { booked_seats: [] };
        }
    }

    static async createBooking(showId, seatIds) {
        const user = JSON.parse(localStorage.getItem('user'));
        const booking = {
            user_id: user.uid,
            show_id: showId,
            seat_ids: seatIds,
            status: 'pending',
            created_at: new Date().toISOString()
        };
        const docRef = await window.fsAddDoc(window.fsCollection(window.firebaseDb, 'bookings'), booking);
        return { booking_id: docRef.id, ...booking };
    }

    static async makePayment(bookingId, amount, method) {
        const docRef = window.fsDoc(window.firebaseDb, 'bookings', bookingId);
        await window.fsUpdateDoc(docRef, {
            status: 'confirmed',
            amount: amount,
            payment_method: method
        });
        
        // Update show's booked seats
        const bookingSnap = await window.fsGetDoc(docRef);
        const booking = bookingSnap.data();
        
        const showRef = window.fsDoc(window.firebaseDb, 'shows', booking.show_id);
        const showSnap = await window.fsGetDoc(showRef);
        let booked_seats = showSnap.data().booked_seats || [];
        booked_seats = [...booked_seats, ...booking.seat_ids];
        
        await window.fsUpdateDoc(showRef, { booked_seats: booked_seats });
        
        return { success: true };
    }

    static async getHistory() {
        const user = JSON.parse(localStorage.getItem('user'));
        const q = window.fsQuery(window.fsCollection(window.firebaseDb, 'bookings'), window.fsWhere('user_id', '==', user.uid));
        const querySnapshot = await window.fsGetDocs(q);
        return querySnapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
    }

    static async cancelBooking(id) {
        const docRef = window.fsDoc(window.firebaseDb, 'bookings', id);
        const bookingSnap = await window.fsGetDoc(docRef);
        if(bookingSnap.exists()) {
            const booking = bookingSnap.data();
            
            // Remove seats from show
            const showRef = window.fsDoc(window.firebaseDb, 'shows', booking.show_id);
            const showSnap = await window.fsGetDoc(showRef);
            if (showSnap.exists()) {
                let booked_seats = showSnap.data().booked_seats || [];
                booked_seats = booked_seats.filter(seat => !booking.seat_ids.includes(seat));
                await window.fsUpdateDoc(showRef, { booked_seats: booked_seats });
            }
            
            // Delete booking
            await window.fsDeleteDoc(docRef);
            return { success: true };
        }
        throw new Error("Booking not found");
    }
}
