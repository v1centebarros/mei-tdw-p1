import { create } from "zustand";
import { persist } from "zustand/middleware";

interface ChatState {
    chatHistory: string[];
    currentResponse: string;
    addChat: (chat: string) => void;
    setCurrentResponse: (response: string) => void;
    clearChat: () => void;
}

export const useChatStore = create<ChatState>()(
    persist(
        (set) => ({
            chatHistory: [],
            currentResponse: "",
            addChat: (chat) =>
                set((state) => ({ chatHistory: [...state.chatHistory, chat] })),
            setCurrentResponse: (response) => set({ currentResponse: response }),
            clearChat: () => set({ chatHistory: [], currentResponse: "" }),
        }),
        {
            name: "chat-storage", // Key for localStorage
        }
    )
);