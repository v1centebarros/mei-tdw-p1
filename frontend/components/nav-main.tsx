"use client"

import {type LucideIcon} from "lucide-react"

import {Collapsible,} from "@/components/ui/collapsible"
import {
    SidebarGroup, SidebarGroupLabel, SidebarMenu, SidebarMenuButton, SidebarMenuItem,
} from "@/components/ui/sidebar"
import Link from "next/link";


interface Props {
    items: {
        title: string
        url: string
        icon?: LucideIcon
        isActive?: boolean
        items?: {
            title: string
            url: string
        }[]
    }[]
}

export function NavMain({items}: Readonly<Props>) {
    return (<SidebarGroup>
            <SidebarGroupLabel>Platform</SidebarGroupLabel>
            <SidebarMenu>
                {items.map((item) => (<Collapsible
                        key={item.title}
                        asChild
                        defaultOpen={item.isActive}
                        className="group/collapsible"
                    >
                        <SidebarMenuItem>
                            <Link href={item.url} passHref>
                                <SidebarMenuButton tooltip={item.title}>

                                    {item.icon && <item.icon/>}
                                    <span>{item.title}</span>

                                </SidebarMenuButton>
                            </Link>
                        </SidebarMenuItem>
                    </Collapsible>))}
            </SidebarMenu>
        </SidebarGroup>)
}
