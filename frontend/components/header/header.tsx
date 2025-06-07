import { ModeSelector } from '@/components/mode-selector';
import { Separator } from '@/components/ui/separator';
import { SidebarTrigger } from '@/components/ui/sidebar';
import { ModeToggle } from '@/components/header/mode-toggle';
import { ConfigDialog } from '@/components/message-config/config-dialog';
import { LanguageToggle } from '@/components/header/language-toggle';

export const Header = () => {
    return (
        <header className="bg-background sticky top-0 z-50 flex h-16 shrink-0 items-center gap-2 border-b px-4">
            <SidebarTrigger />
            <Separator orientation="vertical" className="mx-2 h-4" />
            <ModeSelector />
            <ConfigDialog />
            <div className="ml-auto flex items-center gap-2">
                <ModeToggle />
                <LanguageToggle />
            </div>
        </header>
    );
};
