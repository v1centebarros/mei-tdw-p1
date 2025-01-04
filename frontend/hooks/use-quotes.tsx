import {queryOptions} from "@tanstack/react-query";


const quotesOptions = queryOptions({
    queryKey: ["quotes"],
    queryFn: async () => {
        const res = await fetch("https://www.stands4.com/services/v2/quotes.php")
        return res.json()
    },
})