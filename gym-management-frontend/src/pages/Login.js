// src/pages/Login.js

import React, { useState, useContext } from 'react';
import axios from 'axios';
import { AuthContext } from '../context/AuthContext';
import { useNavigate, Link } from 'react-router-dom';

const Login = () => {
    const [formData, setFormData] = useState({
        phone_number: '',
        password: '',
    });

    const [error, setError] = useState(null);
    const { login } = useContext(AuthContext);
    const navigate = useNavigate();

    const { phone_number, password } = formData;

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        try {
            const response = await axios.post('http://localhost:8000/api/users/login/', formData);
            login(response.data.access, response.data.refresh);
            navigate('/'); // Redirect to Home Page
        } catch (err) {
            setError(err.response?.data || 'Something went wrong');
        }
    };

    return (
        <div style={styles.container}>
            <h2>Login</h2>
            {error && <p style={{ color: 'red' }}>{JSON.stringify(error)}</p>}
            <form onSubmit={handleSubmit} style={styles.form}>
                <div style={styles.inputGroup}>
                    <label>Phone Number:</label>
                    <input
                        type="text"
                        name="phone_number"
                        value={phone_number}
                        onChange={handleChange}
                        required
                        style={styles.input}
                    />
                </div>
                <div style={styles.inputGroup}>
                    <label>Password:</label>
                    <input
                        type="password"
                        name="password"
                        value={password}
                        onChange={handleChange}
                        required
                        minLength="8"
                        style={styles.input}
                    />
                </div>
                <button type="submit" style={styles.button}>
                    Login
                </button>
            </form>
            <p>
                Don't have an account? <Link to="/register">Register Here</Link>
            </p>
        </div>
    );
};

const styles = {
    container: {
        width: '300px',
        margin: '50px auto',
        textAlign: 'center',
    },
    form: {
        display: 'flex',
        flexDirection: 'column',
    },
    inputGroup: {
        marginBottom: '15px',
        textAlign: 'left',
    },
    input: {
        width: '100%',
        padding: '8px',
        marginTop: '5px',
        boxSizing: 'border-box',
    },
    button: {
        padding: '10px',
        backgroundColor: '#28A745',
        color: '#fff',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
    },
};

export default Login;
