import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Lat.ai | AI Recruitment Discovery Engine",
  description: "Production-grade candidate recommendation system featuring forensic audit and career velocity analysis.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full antialiased">
      <body
        className={`${geistSans.variable} ${geistMono.variable} min-h-full flex flex-col bg-slate-50 text-slate-900 font-sans`}
      >
        {/* Main Dashboard Wrapper */}
        <header className="sticky top-0 z-40 w-full border-b bg-white/80 backdrop-blur">
          <div className="flex h-16 items-center justify-between px-8">
            <div className="flex items-center gap-2">
              <span className="text-2xl font-bold tracking-tight text-blue-600">Lat.ai</span>
              <span className="rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-medium text-blue-800">
                Engine v1.0
              </span>
            </div>
            <nav className="flex items-center space-x-6 text-sm font-medium">
              <a href="/" className="transition-colors hover:text-blue-600">Discovery</a>
              <a href="/ingest" className="transition-colors hover:text-blue-600">Ingestion</a>
              <a href="/analytics" className="transition-colors hover:text-blue-600">Pipeline Stats</a>
            </nav>
          </div>
        </header>

        <main className="flex-1 overflow-y-auto">
          <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
            {children}
          </div>
        </main>

        <footer className="border-t bg-white py-6">
          <div className="mx-auto max-w-7xl px-8 text-center text-sm text-slate-500">
            © 2026 Lat.ai Recruitment Systems. Powered by Groq Llama-3.3 70B[cite: 368].
          </div>
        </footer>
      </body>
    </html>
  );
}