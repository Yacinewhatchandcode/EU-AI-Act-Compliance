"use client";
import Link from 'next/link';
import { useState } from 'react';

export default function Header() {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <header className="fixed w-full z-50 glass-panel border-b border-white/10">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-20">
                    <div className="flex-shrink-0 flex items-center gap-3">
                        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-yellow-400 to-yellow-600 flex items-center justify-center text-slate-900 font-bold text-xl shadow-[0_0_15px_rgba(212,175,55,0.5)]">
                            Ω
                        </div>
                        <Link href="/" className="font-display font-bold text-2xl tracking-tight text-white hover:text-yellow-400 transition-colors">
                            OPEN<span className="text-yellow-500">CLAW</span>
                        </Link>
                    </div>

                    <div className="hidden md:flex space-x-8 items-center">
                        <Link href="/" className="text-slate-300 hover:text-yellow-400 px-3 py-2 text-sm font-medium transition-colors border-b-2 border-transparent hover:border-yellow-500">
                            Journal
                        </Link>
                        <Link href="/about" className="text-slate-300 hover:text-yellow-400 px-3 py-2 text-sm font-medium transition-colors border-b-2 border-transparent hover:border-yellow-500">
                            About
                        </Link>
                        <button className="bg-yellow-600 hover:bg-yellow-500 text-white px-5 py-2 rounded-full text-sm font-medium transition-all shadow-lg shadow-yellow-900/20 hover:shadow-yellow-600/40">
                            Subscribe
                        </button>
                    </div>
                </div>
            </div>
        </header>
    );
}
