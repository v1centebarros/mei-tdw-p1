"use client";
import {Input} from "@/components/ui/input";
import {Button} from "@/components/ui/button";
import {useMutation} from "@tanstack/react-query";
import {useSession} from "next-auth/react";
import {useState} from "react";

export default function Page() {

    const {data: session} = useSession()
    const [search, setSearch] = useState("")
    const [results, setResults] = useState([])

    const searchMutation = useMutation({
        mutationKey: ["search"],
        mutationFn: async (query:string) => {
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/contextualsearch?query=${query}`,
                {
                    method: "GET",
                    headers: {
                        "Authorization": `Bearer ${session?.user.accessToken}`,
                    },
                }
            )
            return res.json()
        },
        onSuccess: (data) => {
            setResults(data)
        },
        onError: (error) => {
            console.error(error)
        }
    })

    const handleSearch = async () => {
        await searchMutation.mutateAsync(search)
    }

    return (
        <div>
            <div className={"flex flex-row items-center gap-x-3 py-8"}>
                <Input type="text" placeholder="Search" className={"max-w-xs"} onChange={(e) => setSearch(e.target.value)}/>
                <Button
                    onClick={handleSearch}
                    disabled={searchMutation.isPending}
                >Search</Button>
            </div>

            {searchMutation.isError && <p>Error</p>}
            {searchMutation.isPending && <p>Loading...</p>}
            {searchMutation.isSuccess && <p>Success</p>}
            {results.length > 0 && results.map((result) => (
                <div key={result.file_id}>
                    <p>{result.title}</p>
                    <p>{result.description}</p>
                </div>
            ))}
        </div>
    )
}