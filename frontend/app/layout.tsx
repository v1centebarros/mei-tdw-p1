import type {Metadata} from "next";
import {Geist, Geist_Mono} from "next/font/google";
import "./globals.css";
import {SidebarInset, SidebarProvider, SidebarTrigger} from "@/components/ui/sidebar";
import {AppSidebar} from "@/components/app-sidebar";
import React from "react";
import {Separator} from "@/components/ui/separator";
import {Providers} from "@/providers/providers";
import {FileUpload} from "@/components/file-upload";

const geistSans = Geist({
    variable: "--font-geist-sans",
    subsets: ["latin"],
});

const geistMono = Geist_Mono({
    variable: "--font-geist-mono",
    subsets: ["latin"],
});

export const metadata: Metadata = {
    title: "Odin Library",
    description: "Application to see it all...",
    authors: [{
        url: "https://github.com/v1centebarros",
        name: "v1centebarros"
    }, {url: "https://github.com/marianaAndrad", name: "Mariana Andrade"}],
};

export default function RootLayout({
                                       children,
                                   }: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
        <body
            className={`${geistSans.variable} ${geistMono.variable} antialiased`}
        >
        <Providers>
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
        </Providers>
        </body>
        </html>
    );
}
