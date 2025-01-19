"use client";

import {Input} from "@/components/ui/input";
import {Button} from "@/components/ui/button";
import {useCallback, useEffect, useState} from "react";
import {useSession} from "next-auth/react"
import {EventSourcePolyfill} from "event-source-polyfill";
import {Send} from "lucide-react";

export default function Page() {

    const {data: session} = useSession()
    const [chat, setChat] = useState<string>("")
    const [chatHistory, setChatHistory] = useState<string[]>([])

    useEffect(() => {
        console.log("Chat history updated", chatHistory)
    }, [chatHistory])


    const requestChat = useCallback(async (chat) => {
        // Reset response at the start of a new chat request
        setChatHistory(prev => [...prev, chat]);
        setChat("");
        let response = "";

        const eventSource = new EventSourcePolyfill(
            `${process.env.NEXT_PUBLIC_API_URL}/chat?question=${encodeURIComponent(chat)}`,
            {
                headers: {
                    Authorization: `Bearer ${session?.user.accessToken}`
                }
            }
        );

        let startedConnection = false;

        eventSource.onmessage = (event) => {
            if (event.data === "") {
                if (startedConnection) {
                    setChatHistory(prev => [...prev, response]);
                    eventSource.close();
                } else {
                    startedConnection = true;
                }
            } else {
                // Use functional update to properly accumulate responses
                response = event.data;
            }
        };

        eventSource.onerror = (error) => {
            setChatHistory(prev => [...prev, response]);
            eventSource.close();
        };

        // Cleanup function
        return () => {
            setChatHistory(prev => [...prev, response]);
            eventSource.close();
        };
    }, [session]);

    return (<>
            <div className={"flex flex-col gap-y-4 border border-gray-300 p-4 rounded-md h-full"}>
                <div className={"flex flex-1 flex-col gap-y-2 flex-grow overflow-y-auto p-4 space-y-4"}>
                    {chatHistory.map((chat, index) => (
                        <div key={index} className={`w-7/12 rounded-2xl p-4 flex flex-col gap-y-1 ${index % 2 === 0 ? 'justify-end bg-primary text-white' : 'justify-start border border-gray-300'}`}>
                            <p className={`${index % 2 === 0 ? "text-white": "text-base"} font-bold text-xl`}>{index % 2 === 0 ? 'You' : 'Odin'}</p>
                            <p className={"text-justify text-base"}>{chat}</p>
                        </div>
                    ))}
                </div>

                <div className={"flex flex-row gap-x-2"}>
                    <Input type="text" placeholder="Start chatting with Odin" className={"flex-grow"}
                           onChange={(e) => setChat(e.target.value)}
                           onKeyDown={async (e) => { if (e.key === 'Enter') await requestChat(chat); }}
                           value={chat}
                    />
                    <Button onClick={() => requestChat(chat)}><Send /></Button>
                </div>
            </div>
        </>
    )
}