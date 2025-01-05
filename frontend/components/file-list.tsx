"use client"
import {useSuspenseQuery} from "@tanstack/react-query";
import {filesOptions} from "@/hooks/use-files";
import {useSession} from "next-auth/react";

export function FileList() {
    const {data: session} = useSession()

    const {data} = useSuspenseQuery(filesOptions(session?.user.accessToken));

    return <div>
        {JSON.stringify(data)}
    </div>
}