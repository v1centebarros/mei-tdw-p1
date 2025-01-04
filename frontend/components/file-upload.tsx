"use client";
import {
    Drawer,
    DrawerContent,
    DrawerDescription,
    DrawerHeader,
    DrawerTitle,
    DrawerTrigger
} from "@/components/ui/drawer";
import {Upload} from "lucide-react";
import Dropzone from "shadcn-dropzone";
import {useState} from "react";
import {FileUploadCard} from "@/components/file-upload-card";
import {useSession} from "next-auth/react";

export function FileUpload() {
    const [files, setFiles] = useState<File[]>([]);
    const { data: session } = useSession()


    const deleteFile = (file: File) => {
        setFiles((prevFiles) => prevFiles.filter((f) => f !== file));
    }

    if (!session?.user) {
        return null;
    }
    
    return (
        <Drawer>
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
                    <div className="grid pt-2">
                        {files.map((file) => (
                            <FileUploadCard file={file} key={file.name} onDelete={deleteFile}/>
                        ))}
                    </div>
                </div>
            </DrawerContent>
        </Drawer>
    );
}