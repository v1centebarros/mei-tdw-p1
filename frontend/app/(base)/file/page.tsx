import React, {Suspense} from 'react';
import {dehydrate, HydrationBoundary} from '@tanstack/react-query';
import {getQueryClient} from '@/lib/getQueryClient';
import {FileDetails} from "@/components/file-details";
import {type SearchParams} from 'nuqs/server'
import {fileParamsCache} from "@/lib/searchParams";
import {auth} from "@/lib/auth";
import {fileOptions} from "@/hooks/use-files";
import {Spinner} from "@/components/spinner";

type PageProps = {
    searchParams: Promise<SearchParams>
}

export default async function Page({searchParams}: PageProps) {

    const {filename} = await fileParamsCache.parse(searchParams);
    const session = await auth();

    const queryClient = getQueryClient();

    void queryClient.prefetchQuery(fileOptions(session?.user.accessToken, filename));

    return (
        <HydrationBoundary state={dehydrate(queryClient)}>
            <Suspense fallback={<div className={"w-full mx-auto"}><Spinner size="large" /></div>}>
                <FileDetails/>
            </Suspense>
        </HydrationBoundary>
    );
}