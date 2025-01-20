import { create } from "zustand";
import { persist } from "zustand/middleware";

interface FileDetailsState {
    fontSize: string;
    expanded: boolean;
    hydrated: boolean; // Tracks hydration status
    setFontSize: (size: string) => void;
    toggleExpanded: () => void;
    setHydrated: () => void;
}

export const useFileDetailsStore = create<FileDetailsState>()(
    persist(
        (set) => ({
            fontSize: "prose-lg", // Default font size
            expanded: false, // Default expanded state
            hydrated: false, // Initially not hydrated
            setFontSize: (size) => set({ fontSize: size }),
            toggleExpanded: () => set((state) => ({ expanded: !state.expanded })),
            setHydrated: () => set({ hydrated: true }), // Mark as hydrated
        }),
        {
            name: "file-details-storage", // Key for localStorage
            onRehydrateStorage: () => (state) => {
                // When rehydration finishes, set hydrated to true
                state?.setHydrated();
            },
        }
    )
);
