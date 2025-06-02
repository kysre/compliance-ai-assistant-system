'use client';

import { SidebarInset, SidebarProvider } from '@/components/ui/sidebar';
import { AppSidebar } from '@/components/app-sidebar';
import { Thread } from '@/components/assistant-ui/thread';

import { Header } from '@/components/header/header';
import { ModeProvider } from '@/contexts/ModeContext';
import { MyRuntimeProvider } from '@/app/my-runtime-provider';

export const Assistant = () => {
    return (
        <ModeProvider>
            <MyRuntimeProvider>
                <SidebarProvider>
                    <AppSidebar />
                    <SidebarInset>
                        <Header />
                        <Thread />
                    </SidebarInset>
                </SidebarProvider>
            </MyRuntimeProvider>
        </ModeProvider>
    );
};
