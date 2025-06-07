import wretch from 'wretch';
import Cookies from 'js-cookie';

interface User {
    email: string;
    username: string;
    first_name: string;
    last_name: string;
}

const BASE_URL = 'http://127.0.0.1:8000';

const api = wretch(BASE_URL).accept('application/json');

const login = (username: string, password: string) => {
    return api.post({ username: username, password: password }, '/api/chats/login/');
};

const setAuthToken = (token: string) => {
    Cookies.set('token', token);
};

const setAuthUser = (user: User) => {
    Cookies.set('user', JSON.stringify(user));
};

// TODO: Add logout functionality
const logout = () => {
    Cookies.remove('token');
    Cookies.remove('user');
};

const getAuthToken = () => {
    return Cookies.get('token');
};

const getAuthUser = () => {
    return JSON.parse(Cookies.get('user') || '{}');
};

const register = (email: string, username: string, password: string) => {
    return api.post(
        { email: email, username: username, password: password },
        '/api/chats/register/',
    );
};

export const AuthUtils = {
    login,
    setAuthToken,
    setAuthUser,
    logout,
    getAuthToken,
    getAuthUser,
    register,
};
