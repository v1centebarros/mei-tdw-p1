import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { CheckCircle, FileText, Search, Brain, Shield, Users } from 'lucide-react'
import Image from "next/image"
import Link from "next/link"
import { signIn } from "@/lib/auth"

export default async function Page() {
    return (
        <div className="flex min-h-screen flex-col">
            {/* Hero Section */}
            <header className="flex flex-col items-center justify-center px-4 py-16 text-center lg:py-24">
                <div className="relative mb-8 size-24 lg:size-32">
                    <Image
                        src="/logo.svg"
                        alt="Odin Logo"
                        width={1024}
                        height={1024}
                        className="dark:invert"
                    />
                </div>
                <h1 className="mb-4 text-4xl font-extrabold tracking-tight sm:text-5xl md:text-6xl">
                    Welcome to Odin
                </h1>
                <p className="mx-auto mb-8 max-w-2xl text-xl text-muted-foreground">
                    Your intelligent document management and analysis platform. Extract insights, search effortlessly,
                    and interact with your documents through AI.
                </p>
                <div className="flex flex-col gap-4 sm:flex-row">
                    <form
                        action={async () => {
                            "use server"
                            await signIn()
                        }}
                    >
                        <Button size="lg">
                            Get Started
                        </Button>
                    </form>
                    <Button size="lg" variant="outline" asChild>
                        <Link href="/demo">Watch Demo</Link>
                    </Button>
                </div>
            </header>

            {/* Features Section */}
            <section className="bg-muted/50 px-4 py-16 lg:py-24">
                <div className="mx-auto max-w-6xl">
                    <h2 className="mb-12 text-center text-3xl font-bold tracking-tight sm:text-4xl">
                        Key Features
                    </h2>
                    <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
                        <Card>
                            <CardContent className="flex flex-col items-center p-6 text-center">
                                <FileText className="mb-4 size-12 text-primary"/>
                                <h3 className="mb-2 text-xl font-semibold">File Upload & Analysis</h3>
                                <p className="text-muted-foreground">
                                    Support for multiple document types with automatic text extraction and metadata
                                    identification.
                                </p>
                            </CardContent>
                        </Card>
                        <Card>
                            <CardContent className="flex flex-col items-center p-6 text-center">
                                <Search className="mb-4 size-12 text-primary"/>
                                <h3 className="mb-2 text-xl font-semibold">Smart Search Engine</h3>
                                <p className="text-muted-foreground">
                                    Powerful keyword-based search with intelligent highlighting and document
                                    relationships.
                                </p>
                            </CardContent>
                        </Card>
                        <Card>
                            <CardContent className="flex flex-col items-center p-6 text-center">
                                <Brain className="mb-4 size-12 text-primary"/>
                                <h3 className="mb-2 text-xl font-semibold">AI-Powered Chat</h3>
                                <p className="text-muted-foreground">
                                    Interactive chat interface for querying documents and receiving AI-powered insights.
                                </p>
                            </CardContent>
                        </Card>
                    </div>
                </div>
            </section>

            {/* Target Audience Section */}
            <section className="px-4 py-16 lg:py-24">
                <div className="mx-auto max-w-6xl">
                    <h2 className="mb-12 text-center text-3xl font-bold tracking-tight sm:text-4xl">
                        Who It's For
                    </h2>
                    <div className="grid gap-8 sm:grid-cols-2">
                        <div className="flex items-start gap-4">
                            <Users className="mt-1 size-6 shrink-0 text-primary"/>
                            <div>
                                <h3 className="mb-2 text-xl font-semibold">Researchers & Academics</h3>
                                <p className="text-muted-foreground">
                                    Manage large collections of papers and books with quick access to key insights and
                                    content.
                                </p>
                            </div>
                        </div>
                        <div className="flex items-start gap-4">
                            <Users className="mt-1 size-6 shrink-0 text-primary"/>
                            <div>
                                <h3 className="mb-2 text-xl font-semibold">Students</h3>
                                <p className="text-muted-foreground">
                                    Organize study materials and quickly find relevant sections for assignments and exam
                                    preparation.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Features List Section */}
            <section className="bg-muted/50 px-4 py-16 lg:py-24">
                <div className="mx-auto max-w-6xl">
                    <h2 className="mb-12 text-center text-3xl font-bold tracking-tight sm:text-4xl">
                        Why Choose Odin
                    </h2>
                    <div className="grid gap-4 sm:grid-cols-2">
                        <div className="flex items-center gap-4">
                            <CheckCircle className="size-5 shrink-0 text-primary"/>
                            <span>Support for multiple document types (PDF)</span>
                        </div>
                        <div className="flex items-center gap-4">
                            <CheckCircle className="size-5 shrink-0 text-primary"/>
                            <span>Automatic text extraction and analysis</span>
                        </div>
                        <div className="flex items-center gap-4">
                            <CheckCircle className="size-5 shrink-0 text-primary"/>
                            <span>Advanced search functionality</span>
                        </div>
                        <div className="flex items-center gap-4">
                            <CheckCircle className="size-5 shrink-0 text-primary"/>
                            <span>AI-powered document insights</span>
                        </div>
                        <div className="flex items-center gap-4">
                            <CheckCircle className="size-5 shrink-0 text-primary"/>
                            <span>Secure file storage and management</span>
                        </div>
                        <div className="flex items-center gap-4">
                            <CheckCircle className="size-5 shrink-0 text-primary"/>
                            <span>Intuitive user interface</span>
                        </div>
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="px-4 py-16 text-center lg:py-24">
                <div className="mx-auto max-w-3xl">
                    <h2 className="mb-4 text-3xl font-bold tracking-tight sm:text-4xl">
                        Ready to Get Started?
                    </h2>
                    <p className="mb-8 text-xl text-muted-foreground">
                        Join thousands of researchers, students, and professionals who are already using Odin to unlock
                        insights from their documents.
                    </p>
                    <Button size="lg" asChild>
                        <Link href="/signup">Start Free Trial</Link>
                    </Button>
                </div>
            </section>

            {/* Footer */}
            <footer className="mt-auto border-t bg-muted/50 px-4 py-6">
                <div
                    className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 text-center sm:flex-row sm:text-left">
                    <div className="flex items-center gap-2">
                        <Image
                            src="/logo.png"
                            alt="Odin Logo"
                            width={24}
                            height={24}
                            className="dark:invert"
                        />
                        <span className="text-sm">© 2024 Odin. All rights reserved.</span>
                    </div>
                    <nav className="flex gap-4 text-sm">
                        <Link href="/privacy" className="text-muted-foreground hover:text-foreground">
                            Privacy
                        </Link>
                        <Link href="/terms" className="text-muted-foreground hover:text-foreground">
                            Terms
                        </Link>
                        <Link href="/contact" className="text-muted-foreground hover:text-foreground">
                            Contact
                        </Link>
                    </nav>
                </div>
            </footer>
        </div>
    )
}