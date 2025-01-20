"use client";

import { useSuspenseQuery } from "@tanstack/react-query";
import Markdown from "react-markdown";
import { fileOptions } from "@/hooks/use-files";
import { useQueryStates } from "nuqs";
import { useSession } from "next-auth/react";
import { fileParsers } from "@/lib/searchParams";
import { Badge } from "@/components/ui/badge";
import { toast } from "@/hooks/use-toast";
import { redirect } from "next/navigation";
import { Separator } from "@/components/ui/separator";
import { Button } from "@/components/ui/button";
import { ClipboardCopy, Maximize2, Minimize2, TypeIcon } from "lucide-react";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuLabel,
    DropdownMenuRadioGroup,
    DropdownMenuRadioItem,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { formatRelative } from "date-fns";
import remarkRehype from "remark-rehype";
import remarkGfm from "remark-gfm";
import {useFileDetailsStore} from "@/stores/file-store";
import {Spinner} from "@/components/spinner";
import React from "react";

const fontSizes = [
    { label: "Small", value: "prose-base" },
    { label: "Medium", value: "prose-lg" },
    { label: "Large", value: "prose-xl" },
];

export function FileDetails() {
    const [{ filename }] = useQueryStates(fileParsers);

    if (!filename) {
        toast({ title: "No filename", content: "No filename provided" });
        redirect("/");
    }

    const { data: session } = useSession();
    const { data: fileData, isSuccess } = useSuspenseQuery(
        fileOptions(session?.user.accessToken, filename)
    );

    const { fontSize, expanded, setFontSize, toggleExpanded, hydrated } =
        useFileDetailsStore();

    const copyToClipboard = async () => {
        await navigator.clipboard.writeText(fileData?.content);
        toast({
            title: "Copied to clipboard",
            description: "File content copied to clipboard",
        });
    };

    if (!hydrated) {
        return <div className={"w-full mx-auto"}><Spinner size="large" /></div>
    }

    if (isSuccess)
        return (
            <div className="w-full mx-auto">
                <p>
                    <span className="text-4xl font-bold">{fileData?.filename}</span>
                    <span className="text-lg font-light">{fileData?.content_type}</span>
                </p>

                {fileData?.created_at && (
                    <p>
                        Uploaded{" "}
                        {formatRelative(new Date(fileData?.created_at), new Date())}
                    </p>
                )}

                {fileData?.categories?.map((category: string, index: number) => (
                    <Badge key={index} className="mr-2">
                        {category}
                    </Badge>
                ))}
                <Separator orientation="horizontal" className="my-4" />

                <div className="flex gap-x-1 pb-4">
                    <Button variant="outline" onClick={toggleExpanded}>
                        {expanded ? <Minimize2 /> : <Maximize2 />}
                    </Button>
                    <DropdownMenu>
                        <DropdownMenuTrigger type="button" color="primary" asChild>
                            <Button variant="outline">
                                <TypeIcon />
                            </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent>
                            <DropdownMenuLabel>Font Size</DropdownMenuLabel>
                            <DropdownMenuRadioGroup
                                value={fontSize}
                                onValueChange={setFontSize}
                            >
                                {fontSizes.map(({ label, value }) => (
                                    <DropdownMenuRadioItem value={value} key={value}>
                                        {label}
                                    </DropdownMenuRadioItem>
                                ))}
                            </DropdownMenuRadioGroup>
                        </DropdownMenuContent>
                        <Button onClick={copyToClipboard} variant="outline">
                            <ClipboardCopy />
                        </Button>
                    </DropdownMenu>
                </div>
                <Markdown
                    className={`transition-all duration-1000 ease-in-out mx-auto ${
                        expanded ? "" : "px-48"
                    } min-w-full prose ${fontSize}`}
                    rehypePlugins={[remarkRehype]}
                    remarkPlugins={[remarkGfm]}
                    remarkRehypeOptions={{ passThrough: ["link"] }}
                >
                    {fileData?.content}
                </Markdown>
            </div>
        );
}
