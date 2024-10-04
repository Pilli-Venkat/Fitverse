// src/pages/Register.js

import React, { useState } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';

const Register = () => {
    const [formData, setFormData] = useState({
        phone_number: '',
        email: '',
        name: '',
        role: 'gym_owner',
        password: '',
    });

    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(false);
    const navigate = useNavigate();

    const { phone_number, email, name, role, password } = formData;

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        try {
            const response = await axios.post('http://localhost:8000/api/users/register/', formData);
            console.log(response.data);
            setSuccess(true);
            // Optionally, redirect to login page after successful registration
            setTimeout(() => {
                navigate('/login');
            }, 2000);
        } catch (err) {
            setError(err.response?.data || 'Something went wrong');
        }
    };

    return (
        <div style={styles.container}>
            <h2>Register</h2>
            {success ? (
                <p style={{ color: 'green' }}>
                    Registration successful! Redirecting to <Link to="/login">Login</Link>...
                </p>
            ) : (
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
                        <label>Email:</label>
                        <input
                            type="email"
                            name="email"
                            value={email}
                            onChange={handleChange}
                            required
                            style={styles.input}
                        />
                    </div>
                    <div style={styles.inputGroup}>
                        <label>Name:</label>
                        <input
                            type="text"
                            name="name"
                            value={name}
                            onChange={handleChange}
                            required
                            style={styles.input}
                        />
                    </div>
                    <div style={styles.inputGroup}>
                        <label>Role:</label>
                        <select name="role" value={role} onChange={handleChange} style={styles.input}>
                            <option value="gym_owner">Gym Owner</option>
                            <option value="trainer">Trainer</option>
                            <option value="customer">Customer</option>
                            <option value="manager">Manager</option>
                        </select>
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
                    {error && <p style={{ color: 'red' }}>{JSON.stringify(error)}</p>}
                    <button type="submit" style={styles.button}>
                        Register
                    </button>
                </form>
            )}
            <p>
                Already have an account? <Link to="/login">Login Here</Link>
            </p>
        </div>
    );
};

const styles = {
    container: {
        width: '400px',
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
        backgroundColor: '#17A2B8',
        color: '#fff',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
    },
};

export default Register;
