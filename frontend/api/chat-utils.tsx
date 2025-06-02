import wretch from 'wretch';
import Cookies from 'js-cookie';

const BASE_URL = 'http://127.0.0.1:8080';

const api = wretch(BASE_URL)
    .accept('application/json')
    .auth(`Token ${Cookies.get('token')}`);

const getThreads = () => {
    return api.get('/api/chats/threads/');
};

const getMessages = (threadId: string) => {
    return api.get(`/api/chats/threads/${threadId}/messages/`);
};

const createThread = () => {
    return api.post('/api/chats/threads/');
};

const sendMessage = (threadId: string, message: string) => {
    return api.post({ message }, `/api/chats/threads/${threadId}/messages/`);
};

const query = (ragMode: string, ragType: string, query: string) => {
    return api.post({ query: query, mode: ragMode }, `/api/compliance/query/`);
};

export const ChatUtils = {
    getThreads,
    getMessages,
    createThread,
    sendMessage,
    query,
};
