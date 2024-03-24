import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import firebase from 'firebase/app';
import 'firebase/auth';
import '../App.css';

function Profile() {
    const history = useHistory();
    const [user, setUser] = useState(null);
    const [error, setError] = useState('');

    useEffect(() => {
        firebase.auth().onAuthStateChanged((user) => {
            if (user) {
                setUser({
                    displayName: user.displayName,
                    email: user.email,
                    uid: user.uid,
                });
            } else {
                history.push('/');
            }
        });
    }, [history]);

    const handleLogout = async () => {
        setError('');
        try {
            await firebase.auth().signOut();
            history.push('/');
        } catch (error) {
            setError(error.message);
        }
    };

    return (
        <div className="profile-container">
            <h2>Profile</h2>
            {error && <p className="error">{error}</p>}
            {user && (
                <div className="profile-info">
                    <p><strong>Name:</strong> {user.displayName || 'No name provided'}</p>
                    <p><strong>Email:</strong> {user.email}</p>
                    <p><strong>UID:</strong> {user.uid}</p>
                    <button onClick={handleLogout} className="logout-button">Logout</button>
                </div>
            )}
        </div>
    );
}

export default Profile;
