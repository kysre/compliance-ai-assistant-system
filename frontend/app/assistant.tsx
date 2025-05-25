"use client";

import { SidebarInset, SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/app-sidebar"
import { Thread } from "@/components/assistant-ui/thread";

import { MyRuntimeProvider } from "@/app/MyRuntimeProvider";


export const Assistant = () => {
    return (
        <MyRuntimeProvider>
            <SidebarProvider>
                <AppSidebar />
                <SidebarInset>
                    <header>
                        <SidebarTrigger />
                    </header>
                    <Thread />
                </SidebarInset>
            </SidebarProvider>
        </MyRuntimeProvider>
    );
};
