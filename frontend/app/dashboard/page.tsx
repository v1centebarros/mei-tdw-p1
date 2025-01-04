import {QuoteDisplayer} from "@/components/quote-displayer";
import {Input} from "@/components/ui/input";
import {Button} from "@/components/ui/button";


export default function Page() {
    return (<>

            <h1 className={"text-center text-6xl mx-auto pt-10"}>Pursue Knowledge Today!</h1>
            <QuoteDisplayer/>
            <div className="flex w-full max-w-xl items-center space-x-2">
                <Input placeholder={"Search..."}/>
                <Button type="submit">Subscribe</Button>
            </div>
        </>
    );
}