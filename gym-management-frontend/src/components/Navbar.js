// src/components/Navbar.js

import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

const Navbar = () => {
    const { user, logout } = useContext(AuthContext);

    return (
        <nav style={styles.nav}>
            <Link to="/" style={styles.brand}>
                Gym Management
            </Link>
            <div>
                {user ? (
                    <>
                        <Link to="/dashboard" style={styles.link}>
                            Dashboard
                        </Link>
                        <button onClick={logout} style={styles.button}>
                            Logout
                        </button>
                    </>
                ) : (
                    <>
                        <Link to="/register" style={styles.link}>
                            Register
                        </Link>
                        <Link to="/login" style={styles.link}>
                            Login
                        </Link>
                    </>
                )}
            </div>
        </nav>
    );
};

const styles = {
    nav: {
        padding: '10px 20px',
        backgroundColor: '#343A40',
        color: '#fff',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
    },
    brand: {
        color: '#fff',
        textDecoration: 'none',
        fontSize: '24px',
    },
    link: {
        marginRight: '15px',
        color: '#fff',
        textDecoration: 'none',
    },
    button: {
        padding: '5px 10px',
        backgroundColor: '#DC3545',
        color: '#fff',
        border: 'none',
        borderRadius: '3px',
        cursor: 'pointer',
    },
};

export default Navbar;
