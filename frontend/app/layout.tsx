import "./globals.css";
import {Geist, Geist_Mono} from "next/font/google";
import type {Metadata} from "next";
import React from "react";
import {Providers} from "@/providers/providers";

const geistSans = Geist({
    variable: "--font-geist-sans", subsets: ["latin"],
});

const geistMono = Geist_Mono({
    variable: "--font-geist-mono", subsets: ["latin"],
});

export const metadata: Metadata = {
    title: "Odin Library", description: "Application to see it all...", authors: [{
        url: "https://github.com/v1centebarros", name: "v1centebarros"
    }, {url: "https://github.com/marianaAndrad", name: "Mariana Andrade"}],
};

export default function RootLayout({children}: Readonly<{ children: React.ReactNode; }>) {
    return (<html lang="en">
    <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
    >
    <Providers>

        {children}
    </Providers>
    </body>
    </html>);
}