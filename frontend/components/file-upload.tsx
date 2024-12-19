import {Drawer, DrawerContent, DrawerTitle, DrawerTrigger} from "@/components/ui/drawer";
import {Button} from "@/components/ui/button";

export function FileUpload() {
    return (
        <Drawer>
            <DrawerTitle>Upload File</DrawerTitle>
            <DrawerTrigger asChild>
                <Button variant={"destructive"}>Upload File</Button>
            </DrawerTrigger>
            <DrawerContent>

            </DrawerContent>
        </Drawer>
    );
}