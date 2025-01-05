import {SidebarInset, SidebarProvider, SidebarTrigger} from "@/components/ui/sidebar";
import {AppSidebar} from "@/components/app-sidebar";
import React from "react";
import {Separator} from "@/components/ui/separator";
import {FileUpload} from "@/components/file-upload";

export default function Layout({
                                       children,
                                   }: Readonly<{
    children: React.ReactNode;
}>) {
    return (
            <SidebarProvider>
                <AppSidebar/>
                <SidebarInset>
                    <header className="flex h-16 shrink-0 items-center gap-2 border-b px-4">
                        <SidebarTrigger className="-ml-1"/>
                        <FileUpload/>
                        <Separator orientation="vertical" className="mr-2 h-4"/>
                    </header>
                    <div className="flex flex-1 flex-col gap-4 p-4">
                        {children}
                    </div>
                </SidebarInset>
            </SidebarProvider>
    );
}
