'use client';

import { LoginForm } from '@/components/login-form';
import { useTranslations } from 'next-intl';

export default function Page() {
    const t = useTranslations('Direction');

    return (
        <div dir={t('dir')}>
            <div className="flex min-h-svh w-full items-center justify-center p-6 md:p-10">
                <div className="w-full max-w-sm">
                    <LoginForm />
                </div>
            </div>
        </div>
    );
}
