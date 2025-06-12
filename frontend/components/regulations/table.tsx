'use client';

import { useState, useEffect, useMemo } from 'react';
import { getCoreRowModel, PaginationState, useReactTable } from '@tanstack/react-table';
import { Regulation, RegulationUtils } from '@/api/regulation-utils';
import { useRegulationColumns } from '@/components/regulations/columns';
import { DataTable } from '@/components/regulations/data-table';
import SkeletonTable from '@/components/ui/skeleton-table';

interface RegulationsResponse {
    results: Regulation[];
    count: number;
    next: string | null;
    previous: string | null;
}

export default function RegulationsTable() {
    const columns = useRegulationColumns();
    const [data, setData] = useState<Regulation[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [totalCount, setTotalCount] = useState(0);

    const [{ pageIndex, pageSize }, setPagination] = useState<PaginationState>({
        pageIndex: 0,
        pageSize: 15,
    });

    const pagination = useMemo(
        () => ({
            pageIndex,
            pageSize,
        }),
        [pageIndex, pageSize],
    );

    useEffect(() => {
        const fetchRegulations = async () => {
            try {
                setLoading(true);
                setError(null);

                const response = await RegulationUtils.getRegulations(
                    pageIndex + 1,
                    pageSize,
                ).json<RegulationsResponse>();

                setData(response.results);
                setTotalCount(response.count);
            } catch (err) {
                setError('Failed to fetch regulations');
                console.error('Error fetching regulations:', err);
            } finally {
                setLoading(false);
            }
        };
        fetchRegulations();
    }, [pageIndex, pageSize]);

    const pageCount = useMemo(() => {
        return Math.ceil(totalCount / pageSize);
    }, [totalCount, pageSize]);

    const table = useReactTable({
        data,
        columns,
        pageCount: pageCount ?? -1,
        state: {
            pagination,
        },
        onPaginationChange: setPagination,
        getCoreRowModel: getCoreRowModel(),
        manualPagination: true,
    });

    if (loading) {
        return <SkeletonTable rowCount={pageSize} colCount={columns.length} />;
    }

    if (error) {
        return <div className="flex h-32 items-center justify-center text-red-500">{error}</div>;
    }

    return <DataTable table={table} totalCount={totalCount} />;
}
