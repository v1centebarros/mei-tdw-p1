import {dehydrate, HydrationBoundary} from "@tanstack/react-query";
import {getQueryClient} from "@/lib/getQueryClient";
import {filesOptions} from "@/hooks/use-files";
import {Suspense} from "react";
import {FileList} from "@/components/file-list";
import {auth} from "@/lib/auth";
import {Select, SelectContent, SelectItem, SelectTrigger, SelectValue} from "@/components/ui/select";
import {Input} from "@/components/ui/input";

export default async function Home() {


    const queryClient = getQueryClient();
    const session = await auth();

    void queryClient.prefetchQuery(filesOptions(session?.user.accessToken));

    return (<div className={"container mx-auto"}>
            <p className={"text-5xl text-center"}>My Files</p>
            <div className={"flex flex-row items-center gap-x-3 py-8"}>
                <Input type="email" placeholder="Search" className={"max-w-xs"}/>
                <Select>
                    <SelectTrigger className="w-[180px]">
                        <SelectValue placeholder="Category"/>
                    </SelectTrigger>
                    <SelectContent>
                        <SelectItem value="light">Light</SelectItem>
                        <SelectItem value="dark">Dark</SelectItem>
                        <SelectItem value="system">System</SelectItem>
                    </SelectContent>
                </Select>
            </div>
            <HydrationBoundary state={dehydrate(queryClient)}>
                <Suspense fallback={<p>Loading...</p>}>
                    <FileList/>
                </Suspense>
            </HydrationBoundary>
        </div>
    );
}
