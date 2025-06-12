'use client';

import { SidebarInset, SidebarProvider } from '@/components/ui/sidebar';
import { AppSidebar } from '@/components/app-sidebar';
import { ModeProvider } from '@/contexts/mode-context';
import { ThreadProvider } from '@/contexts/thread-context';
import { ChatWithThreads } from '@/app/runtime/my-external-store-runtime';
import { ConfigProvider } from '@/contexts/config-context';
import { Header } from '@/components/header/header';

export default function DashboardLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <ConfigProvider>
            <ModeProvider>
                <ThreadProvider>
                    <ChatWithThreads>
                        <SidebarProvider>
                            <AppSidebar />
                            <SidebarInset>
                                <Header />
                                {children}
                            </SidebarInset>
                        </SidebarProvider>
                    </ChatWithThreads>
                </ThreadProvider>
            </ModeProvider>
        </ConfigProvider>
    );
}
