"use client";

import { SidebarInset, SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/app-sidebar"
import { Thread } from "@/components/assistant-ui/thread";

import { MyRuntimeProvider } from "@/app/MyRuntimeProvider";
import { Separator } from "@/components/ui/separator";
import { ModeSelector } from "@/components/mode-selector";
import { ModeProvider } from "@/contexts/ModeContext";


export const Assistant = () => {
    return (
        <ModeProvider>
            <MyRuntimeProvider>
                <SidebarProvider>
                    <AppSidebar />
                    <SidebarInset>
                        <header className="flex h-16 shrink-0 items-center gap-2 border-b px-4">
                            <SidebarTrigger />
                            <Separator orientation="vertical" className="mx-2 h-4" />
                            <ModeSelector />
                        </header>
                        <Thread />
                    </SidebarInset>
                </SidebarProvider>
            </MyRuntimeProvider>
        </ModeProvider>
    );
};
