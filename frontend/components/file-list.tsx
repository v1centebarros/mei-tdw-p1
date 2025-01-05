"use client"
import {useSuspenseQuery} from "@tanstack/react-query";
import {filesOptions} from "@/hooks/use-files";
import {useSession} from "next-auth/react";
import {Card, CardContent, CardFooter, CardHeader, CardTitle} from "@/components/ui/card";
import {Button} from "@/components/ui/button";
import Link from "next/link";
import {formatRelative} from "date-fns";

const fileSizeConverter = (size: number) => {
    if (size < 1024) {
        return size + ' Bytes';
    } else if (size < 1048576) {
        return (size / 1024).toFixed(2) + ' KB';
    } else if (size < 1073741824) {
        return (size / 1048576).toFixed(2) + ' MB';
    } else {
        return (size / 1073741824).toFixed(2) + ' GB';
    }
}


export function FileList() {
    const {data: session} = useSession()

    const {data} = useSuspenseQuery(filesOptions(session?.user.accessToken));

    return <div>
        <div className={"grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-4"}>
            {data?.map((file) => (
                <Card key={file.fileId} className={"hover:shadow-lg transition duration-300"}>
                    <CardHeader>
                        <CardTitle className={"truncate ..."}>{file.filename}</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p>{fileSizeConverter(file.size)}</p>
                        <p>{formatRelative(new Date(file.last_modified), new Date())}</p>
                    </CardContent>
                    <CardFooter>
                        <Button className="w-full" asChild>
                            <Link href={`/file?filename=${file.fileId}`}>
                                More Details
                            </Link>
                        </Button>
                    </CardFooter>
                </Card>
            ))
            }
        </div>
    </div>
}