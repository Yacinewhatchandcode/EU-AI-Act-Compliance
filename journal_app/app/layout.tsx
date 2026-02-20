import type { Metadata } from "next";
import { Inter, Outfit } from "next/font/google"; // Changed from Geist
import "./globals.css";

const outfit = Outfit({
  variable: "--font-outfit",
  subsets: ["latin"],
  display: "swap",
});

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "OpenClaw Journal | Cutting Edge Ethical News",
  description: "Faith, Unity, and Technology. Daily updates on EU AI Regulation 2026 and Ethical AI.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${outfit.variable} ${inter.variable} antialiased bg-slate-900 text-slate-100 min-h-screen flex flex-col`}
      >
        {children}
      </body>
    </html>
  );
}
