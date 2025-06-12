'use client';

import { ColumnDef } from '@tanstack/react-table';
import { Regulation } from '@/api/regulation-utils';
import { useTranslations } from 'next-intl';
import Link from 'next/link';

export function useRegulationColumns(): ColumnDef<Regulation>[] {
    const t = useTranslations('RegulationsColumns');

    return [
        {
            accessorKey: 'title',
            header: t('title'),
            cell: ({ row }) => {
                const title = row.getValue('title') as string;
                const { identifier } = row.original;
                const truncatedTitle = title.length > 50 ? `${title.substring(0, 50)}...` : title;

                return (
                    <Link href={`/dashboard/regulations/${identifier}`} className="underline">
                        {truncatedTitle}
                    </Link>
                );
            },
        },
        {
            accessorKey: 'authority',
            header: t('authority'),
        },
        {
            accessorKey: 'date',
            header: t('date'),
        },
        {
            accessorKey: 'link',
            header: t('link'),
            cell: ({ row }) => (
                <a
                    href={row.getValue('link')}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="underline"
                >
                    {t('viewLink')}
                </a>
            ),
        },
    ];
}
