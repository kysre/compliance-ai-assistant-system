import Cookies from 'js-cookie';

const setLocaleInCookie = (locale: string) => {
    Cookies.set('locale', locale);
};

const getLocaleFromCookie = () => {
    return Cookies.get('locale') || 'en';
};

export const ClientUtils = {
    setLocaleInCookie,
    getLocaleFromCookie,
};
