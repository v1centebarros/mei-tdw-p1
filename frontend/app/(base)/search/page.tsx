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
import { Spinner } from "@/components/spinner";

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
        <div className={"flex justify-center gap-x-3 py-8 w-full"}>
            <Input type="text" placeholder="Search" className={"max-w-md"}
                   onChange={(e) => setSearch(e.target.value)}/>

            <Select onValueChange={(value) => setThreshold(parseInt(value))} defaultValue={"128"}>
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
        {isLoading && <div className={"w-full mx-auto"}><Spinner size="large" /></div>}
        {isSuccess && <>
            <p className={"text-3xl"}>Found {results.reduce((acc, result) => acc + result.marked_sentences.length, 0)} occurrences
                in {results.length} files</p>

            <Accordion type={"multiple"} className={"w-full px-16"}>
                {results.map((result, index) => <AccordionItem key={`item_${index}`} value={result.filename}>
                    <AccordionTrigger>{result.filename}</AccordionTrigger>
                    <AccordionContent key={`content_${index}`}>
                        {result.marked_sentences.map((sentence, index) => (<div key={index}>
                            <Separator orientation={"horizontal"} className={"my-2"}/>
                            <div dangerouslySetInnerHTML={{__html: sentence}} className={"prose max-w-full"}/>
                        </div>))}
                    </AccordionContent>
                </AccordionItem>)}
            </Accordion>
        </>}
    </div>)
}
