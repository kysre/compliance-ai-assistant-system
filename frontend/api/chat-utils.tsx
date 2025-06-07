import wretch from 'wretch';
import Cookies from 'js-cookie';

const BASE_URL = 'http://127.0.0.1:8000';

const api = wretch(BASE_URL)
    .accept('application/json')
    .auth(`Token ${Cookies.get('token')}`);

const getThreads = () => {
    return api.get('/api/chats/threads/');
};

const deleteThread = (threadId: string) => {
    return api.delete(`/api/chats/threads/${threadId}/`);
};

const getMessages = (threadId: string) => {
    return api.get(`/api/chats/threads/${threadId}/messages/`);
};

const createThread = () => {
    return api.post({}, '/api/chats/threads/');
};

const sendMessage = (
    threadId: string,
    message: string,
    ragType: string,
    ragMode: string,
    systemPromptType: string,
    customPrompt: string,
) => {
    return api.post(
        {
            message: message,
            type: ragType,
            mode: ragMode,
            system_prompt_type: systemPromptType,
            custom_prompt: customPrompt,
        },
        `/api/chats/threads/${threadId}/messages/`,
    );
};

const query = (ragMode: string, ragType: string, query: string) => {
    return api.post({ query: query, mode: ragMode }, `/api/compliance/query/`);
};

export const ChatUtils = {
    getThreads,
    getMessages,
    createThread,
    deleteThread,
    sendMessage,
    query,
};
