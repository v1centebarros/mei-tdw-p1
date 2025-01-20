"use client"
import {useSuspenseQuery} from "@tanstack/react-query";
import {filesOptions} from "@/hooks/use-files";
import {useSession} from "next-auth/react";
import {Card, CardContent, CardFooter, CardHeader, CardTitle} from "@/components/ui/card";
import {Button} from "@/components/ui/button";
import Link from "next/link";
import {formatRelative} from "date-fns";
import {
    ContextMenu,
    ContextMenuContent,
    ContextMenuItem,
    ContextMenuShortcut,
    ContextMenuTrigger,
} from "@/components/ui/context-menu";
import {Eye, Trash} from "lucide-react";
import {toast} from "@/hooks/use-toast";
import {getQueryClient} from "@/lib/getQueryClient";

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
    const queryClient = getQueryClient();

    const deleteFile = async (fileId: string) => {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/files/${fileId}`, {
            method: 'DELETE',
            headers: {
                Authorization: `Bearer ${session?.user.accessToken}`
            }
        });
        if (response.ok) {
            toast({
                title: 'File Deleted',
                description: 'File deleted successfully'
            })
            await queryClient.invalidateQueries({queryKey: ["files"]})
            console.log('File deleted successfully')
        }
    }


    return <div>
        <div className={"grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-4"}>
            {data.length > 0 && data?.map((file) => (<ContextMenu key={file.fileId}>
                    <ContextMenuTrigger><Card className={"hover:shadow-lg transition duration-300"}>
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
                    </Card></ContextMenuTrigger>
                    <ContextMenuContent>
                        <Link href={`/file?filename=${file.fileId}`}>
                            <ContextMenuItem  className={"hover:cursor-pointer"} inset>
                                View
                                <ContextMenuShortcut><Eye/></ContextMenuShortcut>
                            </ContextMenuItem>
                        </Link>
                        <ContextMenuItem  className={"hover:cursor-pointer"} inset onClick={() => deleteFile(file.fileId)}>
                            Delete
                            <ContextMenuShortcut><Trash/></ContextMenuShortcut>
                        </ContextMenuItem>
                    </ContextMenuContent>
                </ContextMenu>
            ))
            }
        </div>
    </div>
}