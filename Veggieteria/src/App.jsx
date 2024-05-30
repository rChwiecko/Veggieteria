import React, { useState } from 'react';
import './App.css';

const App = () => {
    const [loading, setLoading] = useState(false);
    const [shopSession, setShopSession] = useState(false); 
    const handleSessionClick = () => {
        setLoading(true);
        fetch('http://127.0.0.1:5000/run_script', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ script_name: 'EatingAction' }) // Update the script name accordingly
        })
        .then(response => response.json())
        .then(data => {
            setLoading(false);
            if (data.error) {
                console.error('Script error:', data.error);
            }
        })
        .catch(error => {
            console.error('There was an error running the script!', error);
            setLoading(false);
        });
    };
    const handleShopSessions = () => {
        setShopSession(!shopSession)
    }

    return (
        <>
            <h1>Veggieteria</h1>
            <div className="card">
                {!loading && !shopSession && <button onClick={handleSessionClick}>
                    Start session
                </button>}
                {!loading && !shopSession && <button onClick = {handleShopSessions}>
                  Shop
                </button>}
            </div>
            {shopSession && <div><div className='card'>Welcome to the shop!</div>
                <button onClick={handleShopSessions}>back</button>
            </div>}
            {loading && <div className="spinner"></div>}
        </>
    );
};

export default App;
