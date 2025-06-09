import wretch from 'wretch';
import Cookies from 'js-cookie';

export interface Regulation {
    identifier: string;
    title: string;
    text: string;
    date: string;
    authority: string;
    link: string;
}

const BASE_URL = 'http://127.0.0.1:8000';

const getApiInstance = () => {
    const token = Cookies.get('token');
    return wretch(BASE_URL)
        .accept('application/json')
        .auth(token ? `Token ${token}` : '');
};

const getRegulations = (page: number, pageSize: number) => {
    return getApiInstance().get(`/api/compliance/regulations/?page=${page}&page_size=${pageSize}`);
};

const getRegulation = (identifier: string) => {
    return getApiInstance().get(`/api/compliance/regulations/${identifier}/`);
};

const createRegulation = (regulation: Regulation) => {
    return getApiInstance().post(regulation, '/api/compliance/regulations/');
};

const deleteRegulation = (identifier: string) => {
    return getApiInstance().delete(`/api/compliance/regulations/${identifier}/`);
};

export const RegulationUtils = {
    getRegulations,
    getRegulation,
    createRegulation,
    deleteRegulation,
};
