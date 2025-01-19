"use client";
import {Input} from "@/components/ui/input";
import {useQuery} from "@tanstack/react-query";
import {useSession} from "next-auth/react";
import {useState} from "react";
import {searchOptions} from "@/hooks/use-search";
import {Accordion, AccordionContent, AccordionItem, AccordionTrigger} from "@/components/ui/accordion";
import {Separator} from "@/components/ui/separator";
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectLabel,
    SelectTrigger,
    SelectValue
} from "@/components/ui/select";

export default function Page() {

    const {data: session} = useSession()
    const [search, setSearch] = useState("")
    const [threshold, setThreshold] = useState(128)

    const {
        data: results,
        isLoading,
        isError,
        isSuccess
    } = useQuery(searchOptions((session?.user.accessToken), search, threshold))

    return (<div>
        <p className={"text-5xl text-center"}>Contextual Search</p>
        <div className={"flex flex-row justify-items-center gap-x-3 py-8"}>
            <Input type="text" placeholder="Search" className={"max-w-xs"}
                   onChange={(e) => setSearch(e.target.value)}/>

            <Select onValueChange={(value) => setThreshold(value)} defaultValue={"128"}>
                <SelectTrigger className="w-[180px]">
                    <SelectValue placeholder="Select a threshold"/>
                </SelectTrigger>
                <SelectContent>
                    <SelectGroup>
                        <SelectLabel>Threshold</SelectLabel>
                        <SelectItem value={"128"}>xs</SelectItem>
                        <SelectItem value={"256"}>sm</SelectItem>
                        <SelectItem value={"512"}>md</SelectItem>
                        <SelectItem value={"1024"}>lg</SelectItem>
                    </SelectGroup>
                </SelectContent>
            </Select>
        </div>

        {isError && <p>Error</p>}
        {isLoading && <p>Loading...</p>}
        {isSuccess && <>
            <p className={"text-3xl"}>Found {results.reduce((acc, result) => acc + result.marked_sentences.length, 0)} occurrences
                in {results.length} files</p>

            <Accordion type={"multiple"} collapsible className={"w-full px-16"}>
                {results.map((result, index) => (<AccordionItem key={`item_${index}`} value={result.filename}>
                    <AccordionTrigger>{result.filename}</AccordionTrigger>
                    <AccordionContent>
                        {result.marked_sentences.map((sentence, index) => (<>
                            <Separator orientation={"horizontal"} className={"my-2"}/>
                            <div key={index} dangerouslySetInnerHTML={{__html: sentence}} className={"prose max-w-full"}/>
                        </>))}
                    </AccordionContent>
                </AccordionItem>))}
            </Accordion>
        </>}
    </div>)
}
