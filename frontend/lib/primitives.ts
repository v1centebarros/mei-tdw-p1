import {LayoutDashboard, Library, Search, Sparkles} from "lucide-react";

export const sidebar = {
    navMain: [{
        title: "Dashboard", url: "/dashboard", icon: LayoutDashboard, isActive: true
    }, {
        title: "Search", url: "/search", icon: Search
    }, {
        title: "AI Chat", url: "/chat", icon: Sparkles
    },]
}