import { ModeSelector } from '@/components/mode-selector';
import { Separator } from '@/components/ui/separator';
import { SidebarTrigger } from '@/components/ui/sidebar';
import { ModeToggle } from './mode-toggle';

export const Header = () => {
    return (
        <header className="flex h-16 shrink-0 items-center gap-2 border-b px-4">
            <SidebarTrigger />
            <Separator orientation="vertical" className="mx-2 h-4" />
            <ModeSelector />
            <div className="ml-auto">
                <ModeToggle />
            </div>
        </header>
    );
};
