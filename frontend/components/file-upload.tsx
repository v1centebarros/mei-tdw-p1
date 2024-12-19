import {Drawer, DrawerContent, DrawerTitle, DrawerTrigger} from "@/components/ui/drawer";
import {Button} from "@/components/ui/button";
import {Upload} from "lucide-react";

export function FileUpload() {
    return (
        <Drawer>
            <DrawerTitle hidden>Upload File</DrawerTitle>
            <DrawerTrigger asChild>
                <Upload className="h-4 w-4"/>
            </DrawerTrigger>
            <DrawerContent>

            </DrawerContent>
        </Drawer>
    );
}