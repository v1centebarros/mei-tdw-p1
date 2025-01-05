import { queryOptions} from "@tanstack/react-query";



const filesOptions = (token:string | undefined) => queryOptions({
    queryKey: ["files"],
    queryFn: async () => {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/files`,
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        )
        return res.json()
    },
})

const fileOptions = (token:string | undefined, filename:string) => queryOptions({
    queryKey: ["files", filename],
    queryFn: async () => {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/files/${filename}/metadata`,
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        )
        return res.json()
    },
})

export { filesOptions, fileOptions }