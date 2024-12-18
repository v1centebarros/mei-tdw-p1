import {LayoutDashboard, Library, Search, Sparkles} from "lucide-react";

export const sidebar = {
    user: {
        name: "shadcn", email: "m@example.com", avatar: "/avatars/shadcn.jpg",
    }, navMain: [{
        title: "Dashboard", url: "/", icon: LayoutDashboard, isActive: true
    }, {
        title: "Documents", url: "/documents", icon: Library,
    }, {
        title: "Search", url: "/search", icon: Search
    }, {
        title: "AI Chat", url: "/chat", icon: Sparkles
    },]
}