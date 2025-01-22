import {queryOptions} from "@tanstack/react-query";

const searchOptions = (token:string | undefined, query:string, threshold:number) => queryOptions(
    {
        queryKey: ["search", query, threshold],
        queryFn: async () => {
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/contextualsearch?query=${query}&context_range=${threshold}`,
                {
                    method: "GET",
                    headers: {
                        "Authorization": `Bearer ${token}`,
                    },
                }
            )
            return res.json()
        },
        enabled: query.length > 4,
    }
)

export {searchOptions}