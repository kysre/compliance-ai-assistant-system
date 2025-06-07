'use client';

import { Globe } from 'lucide-react';

import { Button } from '@/components/ui/button';
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { useTranslations } from 'next-intl';
import { ClientUtils } from '@/api/client-utils';

export function LanguageToggle() {
    const t = useTranslations('LanguageToggle');

    const { setLocaleInCookie } = ClientUtils;

    const handleLanguageChange = (selectedLocale: string) => {
        setLocaleInCookie(selectedLocale);
        // Refresh the page to apply the new locale
        window.location.reload();
    };

    return (
        <DropdownMenu>
            <DropdownMenuTrigger asChild>
                <Button variant="outline" size="icon">
                    <Globe className="h-[1.2rem] w-[1.2rem]" />
                    <span className="sr-only">{t('title')}</span>
                </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
                <DropdownMenuItem onClick={() => handleLanguageChange('en')}>
                    {t('en')}
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => handleLanguageChange('fa')}>
                    {t('fa')}
                </DropdownMenuItem>
            </DropdownMenuContent>
        </DropdownMenu>
    );
}
