// app/page.tsx
"use client";

import Link from "next/link";

export default function Home() {
  return (
    <main className="flex flex-col items-center justify-center min-h-screen p-6">
      <h1 className="text-4xl font-bold mb-4">Welcome to Velocity AI 🏎️</h1>
      <p className="text-lg text-muted-foreground mb-6">
        Your Formula 1 chatbot for real-time race insights and stats.
      </p>
      <Link
        href="/chat"
        className="px-6 py-2 text-white bg-red-600 hover:bg-red-700 rounded-lg transition"
      >
        Launch Chatbot
      </Link>
    </main>
  );
}
