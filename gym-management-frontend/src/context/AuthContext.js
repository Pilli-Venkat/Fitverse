// src/context/AuthContext.js

import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [authTokens, setAuthTokens] = useState(() => {
        const access = localStorage.getItem('access_token');
        const refresh = localStorage.getItem('refresh_token');
        return access && refresh ? { access, refresh } : null;
    });

    const [user, setUser] = useState(null);

    const loginUser = (access, refresh) => {
        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);
        setAuthTokens({ access, refresh });
    };

    const logoutUser = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setAuthTokens(null);
        setUser(null);
    };

    useEffect(() => {
        const fetchUser = async () => {
            if (authTokens) {
                try {
                    const response = await axios.get('http://localhost:8000/api/users/me/', {
                        headers: {
                            Authorization: `Bearer ${authTokens.access}`,
                        },
                    });
                    setUser(response.data);
                } catch (err) {
                    console.error('Access token expired, attempting refresh...', err);
                    try {
                        const response = await axios.post('http://localhost:8000/api/users/token/refresh/', {
                            refresh: authTokens.refresh,
                        });
                        const newAccess = response.data.access;
                        localStorage.setItem('access_token', newAccess);
                        setAuthTokens({ access: newAccess, refresh: authTokens.refresh });
                        // Retry fetching user data
                        const retryResponse = await axios.get('http://localhost:8000/api/users/me/', {
                            headers: {
                                Authorization: `Bearer ${newAccess}`,
                            },
                        });
                        setUser(retryResponse.data);
                    } catch (refreshError) {
                        console.error('Refresh token expired or invalid', refreshError);
                        logoutUser();
                    }
                }
            }
        };
        fetchUser();
    }, [authTokens]);

    const contextData = {
        user,
        authTokens,
        login: loginUser,
        logout: logoutUser,
    };

    return <AuthContext.Provider value={contextData}>{children}</AuthContext.Provider>;
};
