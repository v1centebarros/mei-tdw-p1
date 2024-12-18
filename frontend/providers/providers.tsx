"use client"
import {SessionProvider} from "next-auth/react";
import {ThemeProvider} from "@/providers/theme-provider";
import {getQueryClient} from "@/lib/getQueryClient";
import {HydrationBoundary, QueryClientProvider} from "@tanstack/react-query";
import {NuqsAdapter} from "nuqs/adapters/next/app";
import {ReactQueryDevtools} from "@tanstack/react-query-devtools";


export function Providers(
    {children}: { children: React.ReactNode }
) {

    const queryClient = getQueryClient();
    return (
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
            <NuqsAdapter>
                <QueryClientProvider client={queryClient}>
                    <SessionProvider>
                        <HydrationBoundary queryClient={queryClient}>
                            {children}
                        </HydrationBoundary>
                    </SessionProvider>
                    <ReactQueryDevtools/>
                </QueryClientProvider>
            </NuqsAdapter>
        </ThemeProvider>
    );
}