import wretch from 'wretch';
import Cookies from 'js-cookie';

const BASE_URL = 'http://127.0.0.1:8000';

const api = wretch(BASE_URL).accept('application/json');

const login = (username: string, password: string) => {
    console.log(username, password);
    return api.post({ username: username, password: password }, '/api/chats/login/');
};

const setAuthToken = (token: string) => {
    Cookies.set('token', token);
};

// TODO: Add logout functionality
const logout = () => {
    Cookies.remove('token');
};

const getAuthToken = () => {
    return Cookies.get('token');
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
    logout,
    getAuthToken,
    register,
};
