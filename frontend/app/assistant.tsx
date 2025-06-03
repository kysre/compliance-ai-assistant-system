'use client';

import { SidebarInset, SidebarProvider } from '@/components/ui/sidebar';
import { AppSidebar } from '@/components/app-sidebar';
import { Thread } from '@/components/assistant-ui/thread';

import { Header } from '@/components/header/header';
import { ModeProvider } from '@/contexts/ModeContext';
import { ThreadProvider } from '@/contexts/thread-context';
import { ChatWithThreads } from '@/app/my-external-store-runtime';

export const Assistant = () => {
    return (
        <ModeProvider>
            <ThreadProvider>
                <ChatWithThreads>
                    <SidebarProvider>
                        <AppSidebar />
                        <SidebarInset>
                            <Header />
                            <Thread />
                        </SidebarInset>
                    </SidebarProvider>
                </ChatWithThreads>
            </ThreadProvider>
        </ModeProvider>
    );
};
