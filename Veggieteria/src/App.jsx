import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import './App.css';

const socket = io('http://127.0.0.1:5001');

const App = () => {
    const [awaitAddr, changeAwait] = useState(true);
    const [addr, changeAddr] = useState('');
    const [loading, setLoading] = useState(false);
    const [shopSession, setShopSession] = useState(false);
    const [coinCount, setCoinCount] = useState(0);
    const [totalCoinCount, setTotalCoinCount] = useState(0);

    useEffect(() => {
        socket.on('coin_earned', data => {
            setCoinCount(data.coin_count);
            showCoinPopup();
        });

        return () => {
            socket.off('coin_earned');
        };
    }, []);

    const showCoinPopup = () => {
        const popup = document.createElement('div');
        popup.className = 'coin-popup';
        popup.innerText = '+1 Coin!';
        document.body.appendChild(popup);
        console.log("+1")
        setTimeout(() => {
            document.body.removeChild(popup);
        }, 3000);
    };

    const handleSessionClick = () => {
        setLoading(true);
        fetch('http://127.0.0.1:5001/run_script', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ script_name: 'EatingAction' , wallet_addr: addr })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            setLoading(false);
            setTotalCoinCount(coinCount);
            setCoinCount(0);
            if (data.error) {
                console.error('Script error:', data.error);
            } else {
                console.log(data.output);
            }
        })
        .catch(error => {
            console.error('There was an error running the script!', error);
            setLoading(false);
        });
    };

    const handleShopSessions = () => {
        setShopSession(!shopSession);
    };

    const handleChangeAddr = (event) => {
        event.preventDefault();
        const newAddr = event.target.elements.address.value;
        changeAddr(newAddr);
        changeAwait(false);

        setLoading(true);
        fetch('http://127.0.0.1:5001/run_script', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ script_name: 'SetAddr', wallet_addr: addr })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            setLoading(false);
            if (data.error) {
                console.error('Script error:', data.error);
            } else {
                console.log(data.output);
            }
        })
        .catch(error => {
            console.error('There was an error running the script!', error);
            setLoading(false);
        });
    };

    return (
        <>
            <h1>Veggieteria</h1>
            {awaitAddr && <div className='wallet-addr-form'>
                <form onSubmit={handleChangeAddr}>
                    <label>
                        Wallet Address:
                        <input type="text" name="address" />
                    </label>
                    <button type="submit">Submit</button>
                </form>
            </div>}
            {!awaitAddr && <div className="card main-menu">
                {!loading && !shopSession && <button onClick={handleSessionClick}>
                    Start session
                </button>}
                {!loading && !shopSession && <button onClick={handleShopSessions}>
                    Shop
                </button>}
            </div>}
            {shopSession && <div>
                <div className='card'>Welcome to the shop!</div>
                <button onClick={handleShopSessions}>Back</button>
            </div>}
            {loading && 
            <div className='display-screen'>
                <div className='show-coins child-div-display'>
                    Coins earned = {Math.round(coinCount*10)}
                </div>
                <div className='child-div-display'>
                    <div className="spinner"></div>
                </div>
                <div className='child-div-display'>
                    <div className='right-text'>
                        <p>Name: Ryan Chwiecko</p>
                        <p>Age: 20</p>
                        <p>Height: 175cm</p>
                        <p>Weight: 190lbs</p>
                        <p>Concerns: Prevent Colon Cancer</p>
                        <p>Cal Goal: {10*Math.round(coinCount*10 + totalCoinCount*10)}/800kcal</p>
                    </div>
                </div>
            </div>}
        </>
    );
};

export default App;
