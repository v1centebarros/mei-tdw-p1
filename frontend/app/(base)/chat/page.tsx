"use client";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useCallback, useState } from "react";
import { useSession } from "next-auth/react";
import { EventSourcePolyfill } from "event-source-polyfill";
import {Send, Trash} from "lucide-react";
import {useChatStore} from "@/stores/chat-store";

export default function Page() {
    const { data: session } = useSession();
    const {
        chatHistory,
        currentResponse,
        addChat,
        setCurrentResponse,
        clearChat,
    } = useChatStore();

    const [chat, setChat] = useState<string>("");

    const requestChat = useCallback(
        async (chat: string) => {
            addChat(chat);
            setChat("");
            let response = "";

            const eventSource = new EventSourcePolyfill(
                `${process.env.NEXT_PUBLIC_API_URL}/chat?question=${encodeURIComponent(
                    chat
                )}`,
                {
                    headers: {
                        Authorization: `Bearer ${session?.user.accessToken}`,
                    },
                }
            );

            let startedConnection = false;

            eventSource.onmessage = (event) => {
                if (event.data === "") {
                    if (startedConnection) {
                        addChat(response);
                        setCurrentResponse("");
                        eventSource.close();
                    } else {
                        startedConnection = true;
                    }
                } else {
                    response = event.data;
                    setCurrentResponse(response);
                }
            };

            eventSource.onerror = (error) => {
                addChat(response);
                setCurrentResponse("");
                eventSource.close();
            };

            return () => {
                addChat(response);
                setCurrentResponse("");
                eventSource.close();
            };
        },
        [session, addChat, setCurrentResponse]
    );

    return (
        <>
            <div className="flex flex-col gap-y-4 border border-gray-300 p-4 rounded-md min-h-full max-h-fit">
                <div className="flex flex-1 flex-col gap-y-2 flex-grow overflow-y-auto p-4 space-y-4">
                    {chatHistory.map((chat, index) => (
                        <div
                            key={index}
                            className={`w-7/12 rounded-2xl p-4 flex flex-col gap-y-1 ${
                                index % 2 === 0
                                    ? "self-end bg-primary text-white"
                                    : "border border-gray-300"
                            }`}
                        >
                            <p
                                className={`${
                                    index % 2 === 0 ? "text-white" : "text-base"
                                } font-bold text-xl`}
                            >
                                {index % 2 === 0 ? "You" : "Odin"}
                            </p>
                            <p className="text-justify text-base">{chat}</p>
                        </div>
                    ))}

                    {currentResponse.length > 0 && (
                        <div className="w-7/12 rounded-2xl p-4 flex flex-col gap-y-1 border border-gray-300">
                            <p className="font-bold text-xl">Odin</p>
                            <p className="text-justify text-base">{currentResponse}</p>
                        </div>
                    )}
                </div>

                <div className="flex flex-row gap-x-2">
                    <Input
                        type="text"
                        placeholder="Start chatting with Odin"
                        className="flex-grow"
                        onChange={(e) => setChat(e.target.value)}
                        onKeyDown={async (e) => {
                            if (e.key === "Enter") await requestChat(chat);
                        }}
                        value={chat}
                        disabled={currentResponse.length > 0}
                    />
                    <Button
                        onClick={() => requestChat(chat)}
                        disabled={currentResponse.length > 0}
                    >
                        <Send />
                    </Button>
                    <Button onClick={clearChat}><Trash/></Button>
                </div>
            </div>
        </>
    );
}