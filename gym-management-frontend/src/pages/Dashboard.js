// src/pages/Dashboard.js

import React, { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { Link } from 'react-router-dom';

const Dashboard = () => {
    const { user, logout } = useContext(AuthContext);

    if (!user) {
        return null; // Or a loading spinner
    }

    return (
        <div style={styles.container}>
            <h2>Dashboard</h2>
            <p>Welcome, {user.name}!</p>
            <p>Your role: {user.role}</p>

            {/* Add role-specific links or functionalities here */}
            {user.role === 'gym_owner' && (
                <Link to="/add-gym" style={styles.link}>
                    Add Gym Details
                </Link>
            )}
            {user.role === 'trainer' && (
                <Link to="/add-trainer-profile" style={styles.link}>
                    Add Trainer Profile
                </Link>
            )}
            {/* Add more role-specific links as needed */}

            <button onClick={logout} style={styles.button}>
                Logout
            </button>
        </div>
    );
};

const styles = {
    container: {
        width: '500px',
        margin: '50px auto',
        textAlign: 'center',
    },
    link: {
        display: 'block',
        margin: '10px 0',
        padding: '10px',
        backgroundColor: '#FFC107',
        color: '#000',
        textDecoration: 'none',
        borderRadius: '5px',
    },
    button: {
        marginTop: '20px',
        padding: '10px',
        backgroundColor: '#DC3545',
        color: '#fff',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
    },
};

export default Dashboard;
