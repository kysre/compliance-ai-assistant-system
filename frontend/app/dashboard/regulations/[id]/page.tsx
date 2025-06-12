'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import type { Regulation } from '@/api/regulation-utils';
import { RegulationUtils } from '@/api/regulation-utils';
import { Separator } from '@/components/ui/separator';
import { useTranslations } from 'next-intl';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { toast } from 'sonner';

export default function Page() {
    // TODO: Add error page on 404 error
    // TODO: Add a confirmation dialog for deleting a regulation
    // TODO: Add a success message after deleting a regulation & redirect to the regulations page

    const tDir = useTranslations('Direction');
    const t = useTranslations('RegulationPage');
    const { id } = useParams();
    const { getRegulation, deleteRegulation } = RegulationUtils;
    const [regulation, setRegulation] = useState<Regulation | undefined>();
    const router = useRouter();

    useEffect(() => {
        if (id) {
            getRegulation(id as string)
                .notFound(() => {
                    toast.error('Requested regulation not found', {
                        description: 'You will be redirected to the regulations page',
                    });
                    setTimeout(() => {
                        router.push('/dashboard/regulations');
                    }, 2000);
                })
                .json((json) => {
                    setRegulation(json.regulation);
                })
                .catch((error) => {
                    toast.error('Error in fetching regulation', {
                        description: 'You will be redirected to the regulations page',
                    });
                    setTimeout(() => {
                        router.push('/dashboard/regulations');
                    }, 2000);
                });
        }
    }, [id]);

    return (
        <div dir={tDir('dir')} className="container mx-auto py-10 lg:px-40">
            <h1 className="my-4 scroll-m-20 text-2xl font-bold tracking-tight">
                {regulation?.title || <Skeleton className="h-8 w-3/4" />}
            </h1>

            <div className="my-2 flex flex-row justify-between">
                {regulation?.authority ? (
                    <h3 className="scroll-m-20 text-lg font-semibold tracking-tight">
                        {regulation.authority}
                    </h3>
                ) : (
                    <Skeleton className="h-6 w-1/4" />
                )}
                {regulation?.date ? (
                    <h3 className="scroll-m-20 text-lg font-semibold tracking-tight">
                        {regulation.date}
                    </h3>
                ) : (
                    <Skeleton className="h-6 w-1/4" />
                )}
            </div>

            <Separator />

            {regulation?.text ? (
                <p className="my-5 text-justify leading-7 [&:not(:first-child)]:mt-6">
                    {regulation.text}
                </p>
            ) : (
                <div className="my-5 space-y-2">
                    <Skeleton className="h-4 w-full" />
                    <Skeleton className="h-4 w-full" />
                    <Skeleton className="h-4 w-[95%]" />
                    <Skeleton className="h-4 w-full" />
                    <Skeleton className="h-4 w-full" />
                    <Skeleton className="h-4 w-full" />
                    <Skeleton className="h-4 w-[90%]" />
                    <Skeleton className="h-4 w-[80%]" />
                </div>
            )}

            {regulation && (
                <>
                    <Separator />
                    <div className="my-2 flex flex-row justify-between">
                        <Button variant="outline">
                            <a href={regulation.link} target="_blank" rel="noopener noreferrer">
                                {t('source')}
                            </a>
                        </Button>
                        <Button
                            variant="destructive"
                            onClick={() => deleteRegulation(id as string)}
                        >
                            {t('delete')}
                        </Button>
                    </div>
                </>
            )}
        </div>
    );
}
