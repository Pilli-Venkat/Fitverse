// src/pages/Home.js

import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

const Home = () => {
    const { user } = useContext(AuthContext);

    if (user) {
        // User is authenticated
        if (user.role === 'customer') {
            return (
                <div style={styles.container}>
                    <h1>Hello, {user.name}!</h1>
                    <p>Welcome back to our Gym Management System.</p>
                    <Link to="/dashboard">Go to Dashboard</Link>
                </div>
            );
        } else if (user.role === 'gym_owner') {
            return (
                <div style={styles.container}>
                    <h1>Hello, {user.name}!</h1>
                    <p>Welcome back! Please register your gym details.</p>
                    <Link to="/dashboard">Go to Dashboard</Link>
                </div>
            );
        } else if (user.role === 'trainer') {
            return (
                <div style={styles.container}>
                    <h1>Hello, {user.name}!</h1>
                    <p>Welcome back! Please update your trainer profile.</p>
                    <Link to="/dashboard">Go to Dashboard</Link>
                </div>
            );
        } else if (user.role === 'manager') {
            return (
                <div style={styles.container}>
                    <h1>Hello, {user.name}!</h1>
                    <p>Welcome back! You can manage approvals here.</p>
                    <Link to="/dashboard">Go to Dashboard</Link>
                </div>
            );
        } else {
            return (
                <div style={styles.container}>
                    <h1>Hello, {user.name}!</h1>
                    <p>Your role is not recognized.</p>
                    <Link to="/dashboard">Go to Dashboard</Link>
                </div>
            );
        }
    }

    // User is not authenticated
    return (
        <div style={styles.container}>
            <h1>Welcome to Gym Management System</h1>
            <div style={styles.buttonContainer}>
                <Link to="/register" style={styles.button}>
                    Register
                </Link>
                <Link to="/login" style={styles.button}>
                    Login
                </Link>
            </div>
        </div>
    );
};

const styles = {
    container: {
        textAlign: 'center',
        marginTop: '50px',
    },
    buttonContainer: {
        marginTop: '20px',
    },
    button: {
        margin: '0 10px',
        padding: '10px 20px',
        backgroundColor: '#007BFF',
        color: '#fff',
        textDecoration: 'none',
        borderRadius: '5px',
    },
};

export default Home;
