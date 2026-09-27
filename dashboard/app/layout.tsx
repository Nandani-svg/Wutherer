import type { Metadata } from "next";
// @ts-expect-error Next.js handles CSS side-effect imports at build time.
import "./globals.css";
// @ts-expect-error Next.js handles CSS side-effect imports at build time.
import "./landing.css"

export const metadata: Metadata = {
    title: "Wutherer",
    description: "Wutherer controls for Discord server safety, community workflows and automation.",
};

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en" className="dark">
            <body className="min-h-screen bg-background text-foreground antialiased selection:bg-primary selection:text-white">
                {children}
            </body>
        </html>
    );
}