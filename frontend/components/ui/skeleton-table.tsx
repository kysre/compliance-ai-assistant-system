import { Skeleton } from '@/components/ui/skeleton';
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '@/components/ui/table';

interface SkeletonTableProps {
    rowCount?: number;
    colCount?: number;
}

export default function SkeletonTable({ rowCount = 3, colCount = 4 }: SkeletonTableProps) {
    return (
        <div className="rounded-lg border">
            <Table>
                <TableHeader>
                    <TableRow>
                        {[...Array(colCount)].map((_, i) => (
                            <TableHead key={i}>
                                <Skeleton className="h-3 w-full" />
                            </TableHead>
                        ))}
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {[...Array(rowCount)].map((_, i) => (
                        <TableRow key={i}>
                            {[...Array(colCount)].map((_, j) => (
                                <TableCell key={j}>
                                    <Skeleton className="h-5 w-full" />
                                </TableCell>
                            ))}
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </div>
    );
}
