'use client';

import { SidebarInset, SidebarProvider } from '@/components/ui/sidebar';
import { AppSidebar } from '@/components/app-sidebar';
import { Thread } from '@/components/assistant-ui/thread';

import { Header } from '@/components/header/header';
import { ModeProvider } from '@/contexts/mode-context';
import { ThreadProvider } from '@/contexts/thread-context';
import { ChatWithThreads } from '@/app/my-external-store-runtime';
import { ConfigProvider } from '@/contexts/config-context';

export const Assistant = () => {
    return (
        <ConfigProvider>
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
        </ConfigProvider>
    );
};
