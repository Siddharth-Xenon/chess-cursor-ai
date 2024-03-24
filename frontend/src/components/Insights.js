import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import firebase from 'firebase/app';
import 'firebase/auth';
import '../App.css';

function Insights() {
    const history = useHistory();
    const [user, setUser] = useState(null);
    const [insights, setInsights] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        firebase.auth().onAuthStateChanged((user) => {
            if (user) {
                setUser({
                    displayName: user.displayName,
                    email: user.email,
                    uid: user.uid,
                });
                // Fetch insights after confirming user is logged in
                fetchInsights();
            } else {
                history.push('/');
            }
        });
    }, [history]);

    const fetchInsights = async () => {
        setLoading(true);
        setError('');
        try {
            // Simulate fetching insights from the server
            // In a real app, you would make an API call to your backend
            // For demonstration, we'll just use a setTimeout
            const fakeInsights = await new Promise((resolve) => setTimeout(() => resolve([
                { move: 'e4', evaluation: 'Good', comment: 'Opening move' },
                { move: 'e5', evaluation: 'Excellent', comment: 'Best response' },
                { move: 'Qh5', evaluation: 'Bad', comment: 'Weak move exposing the queen early' },
            ]), 1000));
            setInsights(fakeInsights);
        } catch (error) {
            setError('Failed to fetch insights. Please try again.');
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="insights-container">
            <h2>Game Insights</h2>
            {error && <p className="error">{error}</p>}
            {loading ? (
                <p>Loading insights...</p>
            ) : (
                <div className="insights-list">
                    {insights.map((insight, index) => (
                        <div key={index} className="insight-item">
                            <p><strong>Move:</strong> {insight.move}</p>
                            <p><strong>Evaluation:</strong> {insight.evaluation}</p>
                            <p><strong>Comment:</strong> {insight.comment}</p>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default Insights;
