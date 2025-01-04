import {Card, CardTitle} from "@/components/ui/card";
import {File, Trash} from "lucide-react";
import {Button} from "@/components/ui/button";
export function FileUploadCard({file, onDelete}: Readonly<{ file: File; onDelete: (f:File) => void}>) {
    return (
        <Card className="flex items-center px-3 h-16 justify-between">
            <File className="h-6 w-6 text-red-500"/>
            <CardTitle>{file.name}</CardTitle>
            <Button variant={"destructive"} onClick={() => onDelete(file)}>
                <Trash className="h-4 w-4"/>
            </Button>
        </Card>

    );
}