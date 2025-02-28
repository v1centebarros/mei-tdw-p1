"use client"
import {SessionProvider} from "next-auth/react";
import {getQueryClient} from "@/lib/getQueryClient";
import {HydrationBoundary, QueryClientProvider} from "@tanstack/react-query";
import {NuqsAdapter} from "nuqs/adapters/next/app";
import {ReactQueryDevtools} from "@tanstack/react-query-devtools";
import {Toaster} from "@/components/ui/toaster";


export function Providers({children}: { children: React.ReactNode }) {

    const queryClient = getQueryClient();
    return (

        <NuqsAdapter>
            <QueryClientProvider client={queryClient}>
                <SessionProvider>
                    <HydrationBoundary queryClient={queryClient}>
                        {children}
                        <Toaster/>
                    </HydrationBoundary>
                </SessionProvider>
                {/* {process.env.NODE_ENV === "development" && <ReactQueryDevtools initialIsOpen={false}/>} */}

            </QueryClientProvider>
        </NuqsAdapter>
    );
}