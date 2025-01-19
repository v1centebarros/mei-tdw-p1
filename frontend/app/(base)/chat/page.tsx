"use client";

import {Input} from "@/components/ui/input";
import {Button} from "@/components/ui/button";
import {useState} from "react";
import { useSession } from "next-auth/react"
import {EventSourcePolyfill} from "event-source-polyfill";

export default function Page() {

    const [chat, setChat] = useState("")
    const [response, setResponse] = useState("")
    const { data: session } = useSession()

    const requestChat = async (chat) => {
        const eventSource = new EventSourcePolyfill(`${process.env.NEXT_PUBLIC_API_URL}/chat?question=${chat}`, {
            headers: {
                Authorization: `Bearer ${session?.user.accessToken}`
            }
        });

        let startedConnection = false;

        eventSource.onmessage = (event) => {
            console.log(event.data);
            if (event.data === "") {
                if (startedConnection) {
                    eventSource.close();
                } else {
                    startedConnection = true;
                }
            } else {
                setResponse(response + event.data);
            }
        }
    }
    return (<>
            <p>Chat</p>
            <p>{JSON.stringify(response)}</p>
            <Input type="text" placeholder="Chat" className={"max-w-xs"} onChange={(e) => setChat(e.target.value)}/>
            <Button onClick={() => requestChat(chat)}>Send</Button>
        </>
    )
}