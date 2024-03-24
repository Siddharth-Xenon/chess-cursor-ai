import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import firebase from 'firebase/app';
import 'firebase/auth';
import '../App.css';

function GameUpload() {
    const history = useHistory();
    const [file, setFile] = useState(null);
    const [error, setError] = useState('');
    const [uploading, setUploading] = useState(false);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleUpload = async (e) => {
        e.preventDefault();
        if (!file) {
            setError('Please select a PGN file to upload.');
            return;
        }
        setError('');
        setUploading(true);

        // Simulate file upload process
        try {
            // Here you would typically upload the file to your server
            // For demonstration, we'll just wait for 2 seconds
            await new Promise((resolve) => setTimeout(resolve, 2000));

            // After uploading, redirect to the insights page
            history.push('/insights');
        } catch (error) {
            setError('Failed to upload the file. Please try again.');
            console.error(error);
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="game-upload-container">
            <h2>Upload Game</h2>
            <form onSubmit={handleUpload} className="game-upload-form">
                {error && <p className="error">{error}</p>}
                <div className="form-group">
                    <label htmlFor="pgnFile">PGN File</label>
                    <input
                        type="file"
                        id="pgnFile"
                        accept=".pgn"
                        onChange={handleFileChange}
                        disabled={uploading}
                    />
                </div>
                <button type="submit" className="upload-button" disabled={uploading}>
                    {uploading ? 'Uploading...' : 'Upload'}
                </button>
            </form>
        </div>
    );
}

export default GameUpload;
