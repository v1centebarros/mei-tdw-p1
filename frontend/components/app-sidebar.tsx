"use client"
import * as React from "react"
import {NavMain} from "@/components/nav-main"
import {NavUser} from "@/components/nav-user"
import {
    Sidebar,
    SidebarContent,
    SidebarFooter,
    SidebarHeader,
    SidebarMenu,
    SidebarMenuButton,
    SidebarRail,
} from "@/components/ui/sidebar"
import Image from "next/image";
import {sidebar} from "@/lib/primitives";
import SignIn from "@/components/sign-in";
import {useSession} from "next-auth/react";

export function AppSidebar({...props}: React.ComponentProps<typeof Sidebar>) {

    const {status, data:session} = useSession();

    return (<Sidebar collapsible="icon" {...props}>
        <SidebarHeader>
            <SidebarMenu>
                <SidebarMenuButton
                    size="lg"
                    className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
                >
                    <div
                        className="flex aspect-square size-8 items-center justify-center rounded-lg text-sidebar-primary-foreground">
                        {/*<activeTeam.logo className="size-4" />*/}
                        <Image src={"/logo.svg"} alt={"Odin Library"} width={128} height={128}/>
                    </div>
                    <div className="grid flex-1 text-left text-sm leading-tight">
                        <span className="truncate font-semibold">
                          Odin Library
                        </span>
                        <span className="truncate text-xs">Beta</span>
                    </div>
                </SidebarMenuButton>
            </SidebarMenu>
        </SidebarHeader>
        <SidebarContent>
            <NavMain items={sidebar.navMain}/>
        </SidebarContent>
        <SidebarFooter>

            {status === "authenticated" && <NavUser user={session?.user}/>}
            {status === "unauthenticated" && <SignIn/>}

            {/*<NavUser user={sidebar.user}/>*/}
        </SidebarFooter>
        <SidebarRail/>
    </Sidebar>)
}