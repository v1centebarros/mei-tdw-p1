"use client"
import * as React from "react"
import {
    BookOpen, Bot, Frame, Map, PieChart, Settings2, SquareTerminal,
} from "lucide-react"
import {NavMain} from "@/components/nav-main"
import {NavUser} from "@/components/nav-user"
import {
    Sidebar, SidebarContent, SidebarFooter, SidebarHeader, SidebarMenu, SidebarMenuButton, SidebarRail,
} from "@/components/ui/sidebar"
import Image from "next/image";

const data = {
    user: {
        name: "shadcn", email: "m@example.com", avatar: "/avatars/shadcn.jpg",
    }, navMain: [{
        title: "Playground", url: "#", icon: SquareTerminal, isActive: true, items: [{
            title: "History", url: "#",
        }, {
            title: "Starred", url: "#",
        }, {
            title: "Settings", url: "#",
        },],
    }, {
        title: "Models", url: "#", icon: Bot, items: [{
            title: "Genesis", url: "#",
        }, {
            title: "Explorer", url: "#",
        }, {
            title: "Quantum", url: "#",
        },],
    }, {
        title: "Documentation", url: "#", icon: BookOpen, items: [{
            title: "Introduction", url: "#",
        }, {
            title: "Get Started", url: "#",
        }, {
            title: "Tutorials", url: "#",
        }, {
            title: "Changelog", url: "#",
        },],
    }, {
        title: "Settings", url: "#", icon: Settings2, items: [{
            title: "General", url: "#",
        }, {
            title: "Team", url: "#",
        }, {
            title: "Billing", url: "#",
        }, {
            title: "Limits", url: "#",
        },],
    },], projects: [{
        name: "Design Engineering", url: "#", icon: Frame,
    }, {
        name: "Sales & Marketing", url: "#", icon: PieChart,
    }, {
        name: "Travel", url: "#", icon: Map,
    },],
}

export function AppSidebar({...props}: React.ComponentProps<typeof Sidebar>) {
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
                <NavMain items={data.navMain}/>
            </SidebarContent>
            <SidebarFooter>
                <NavUser user={data.user}/>
            </SidebarFooter>
            <SidebarRail/>
        </Sidebar>)
}