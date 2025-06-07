'use client';

import {
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from '@radix-ui/react-dropdown-menu';
import { DropdownMenu } from '@/components/ui/dropdown-menu';
import {
    SidebarFooter,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
    useSidebar,
} from '@/components/ui/sidebar';
import { BadgeCheck, ChevronsUpDown, LogOut } from 'lucide-react';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { AuthUtils } from '@/api/auth-utils';
import { useRouter } from 'next/navigation';

export const MySidebarFooter = () => {
    const { isMobile } = useSidebar();
    const router = useRouter();
    const { logout, getAuthUser } = AuthUtils;

    const user = getAuthUser();
    // TODO: Get avatar from backend
    const avatar_source = 'https://github.com/shadcn.png';

    const handleLogout = () => {
        logout();
        router.push('/login');
    };

    const handleAccount = () => {
        // TODO: Implement account modal
    };

    return (
        <SidebarFooter>
            <SidebarMenu>
                <SidebarMenuItem>
                    <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                            <SidebarMenuButton
                                size="lg"
                                className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
                            >
                                <Avatar className="h-8 w-8 rounded-lg">
                                    <AvatarImage src={avatar_source} alt={user.first_name} />
                                    <AvatarFallback className="rounded-lg">CN</AvatarFallback>
                                </Avatar>
                                <div className="grid flex-1 text-left text-sm leading-tight">
                                    <span className="truncate font-medium">{user.first_name}</span>
                                    <span className="truncate text-xs">{user.email}</span>
                                </div>
                                <ChevronsUpDown className="ml-auto size-4" />
                            </SidebarMenuButton>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent
                            className="bg-sidebar-accent text-sidebar-accent-foreground w-(--radix-dropdown-menu-trigger-width) min-w-56 rounded-lg"
                            side={isMobile ? 'bottom' : 'right'}
                            align="end"
                            sideOffset={4}
                        >
                            <DropdownMenuLabel className="border-sidebar-accent rounded-lg border-2 p-1 font-normal">
                                <div className="flex items-center gap-2 px-1 py-1.5 text-left text-sm">
                                    <Avatar className="h-8 w-8 rounded-lg">
                                        <AvatarImage src={avatar_source} alt={user.first_name} />
                                        <AvatarFallback className="rounded-lg">CN</AvatarFallback>
                                    </Avatar>
                                    <div className="grid flex-1 text-left text-sm leading-tight">
                                        <span className="truncate font-medium">
                                            {user.first_name}
                                        </span>
                                        <span className="truncate text-xs">{user.email}</span>
                                    </div>
                                </div>
                            </DropdownMenuLabel>
                            <DropdownMenuSeparator />
                            <DropdownMenuItem
                                onClick={handleAccount}
                                className="border-sidebar-accent hover:bg-sidebar hover:text-foreground cursor-pointer rounded-lg border-2 p-1"
                            >
                                <div className="flex items-center gap-2 px-1 py-1.5 text-left text-sm">
                                    <BadgeCheck className="h-5 w-5 rounded-lg" />
                                    <span>Account</span>
                                </div>
                            </DropdownMenuItem>
                            <DropdownMenuSeparator />
                            <DropdownMenuItem
                                onClick={handleLogout}
                                className="border-sidebar-accent hover:bg-sidebar hover:text-foreground cursor-pointer rounded-lg border-2 p-1"
                            >
                                <div className="flex items-center gap-2 px-1 py-1.5 text-left text-sm">
                                    <LogOut className="h-5 w-5 rounded-lg" />
                                    <span>Log out</span>
                                </div>
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>
                </SidebarMenuItem>
            </SidebarMenu>
        </SidebarFooter>
    );
};
