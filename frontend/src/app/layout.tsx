import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Decision Intelligence System | Multi-Agent AI",
  description: "Production-ready Multi-Agent AI system for strategic business decisions. Powered by RAG, LangGraph, and GPT-4.",
  keywords: ["AI", "Decision Intelligence", "Multi-Agent", "RAG", "LangGraph"],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
