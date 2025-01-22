"use client";
import {
    Drawer,
    DrawerClose,
    DrawerContent,
    DrawerDescription,
    DrawerFooter,
    DrawerHeader,
    DrawerTitle,
    DrawerTrigger
} from "@/components/ui/drawer";
import {Upload} from "lucide-react";
import Dropzone from "shadcn-dropzone";
import {useState} from "react";
import {FileUploadCard} from "@/components/file-upload-card";
import {useSession} from "next-auth/react";
import {useMutation} from "@tanstack/react-query";
import {Button} from "@/components/ui/button";
import {useToast} from "@/hooks/use-toast";
import {getQueryClient} from "@/lib/getQueryClient";
import {Spinner} from "@/components/spinner";

export function FileUpload() {
    const [files, setFiles] = useState<File[]>([]);
    const {data: session} = useSession()
    const {toast} = useToast();
    const queryClient = getQueryClient();

    const filesUploadMutation = useMutation({
        mutationFn: async (files: File[]) => {
            const formData = new FormData();
            files.forEach((file) => {
                formData.append("files", file);
            });

            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/upload/bulk`, {
                method: "POST", body: formData,
                headers: {
                    Authorization: `Bearer ${session?.user?.accessToken}`,
                },
            });
            return response.json();
        }, onSuccess: async () => {
            setFiles([]);
            toast({
                title: "Files uploaded successfully",
                description: "The files were uploaded successfully",
            })
            await queryClient.invalidateQueries({queryKey:["files"]});

        }, onError: (error) => {
            toast({
                title: "Error uploading files",
                description: error.message,
            })
        }
    })

    const onSubmit = () => filesUploadMutation.mutate(files);

    const deleteFile = (file: File) => {
        setFiles((prevFiles) => prevFiles.filter((f) => f !== file));
    }

    if (!session?.user) {
        return null;
    }

    return (<Drawer>
        <DrawerTrigger asChild>
            <Upload className="h-4 w-4"/>
        </DrawerTrigger>
        <DrawerContent>
            <div className="mx-auto w-full max-w-sm min-h-96">
                <DrawerHeader>
                    <DrawerTitle>Upload File</DrawerTitle>
                    <DrawerDescription>Drop files here to upload</DrawerDescription>
                </DrawerHeader>
                <Dropzone
                    dropZoneClassName={"p-4 border-dashed border-2 border-gray-200 rounded-lg hover:bg-accent hover:text-accent-foreground transition-all select-none cursor-pointer"}
                    onDrop={(acceptedFiles: File[]) => {
                        setFiles((prevFiles) => [...prevFiles, ...acceptedFiles]);
                    }}
                    showFilesList={true}
                />
                <div className="flex flex-col gap-y-2 pt-2">
                    {files.map((file) => (<FileUploadCard file={file} key={file.name} onDelete={deleteFile}/>))}
                </div>
                {filesUploadMutation.isPending && <Spinner size="large" />}
                <DrawerFooter>
                    <DrawerClose asChild>
                        <Button onClick={onSubmit}>Submit</Button>
                    </DrawerClose>
                </DrawerFooter>
            </div>
        </DrawerContent>
    </Drawer>);
}