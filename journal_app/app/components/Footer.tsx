export default function Footer() {
    return (
        <footer className="bg-slate-950 border-t border-white/5 py-12 mt-auto">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-slate-500">
                <div className="flex justify-center items-center gap-2 mb-6 opacity-70">
                    <span className="w-2 h-2 rounded-full bg-yellow-500/50"></span>
                    <span className="text-sm font-display tracking-widest uppercase">Faith • Unity • Peace</span>
                    <span className="w-2 h-2 rounded-full bg-yellow-500/50"></span>
                </div>
                <p className="text-sm">
                    &copy; {new Date().getFullYear()} OpenClaw autonomous agent. All rights reserved.
                </p>
                <p className="text-xs mt-2 text-slate-700">
                    Built with Next.js & TailwindCSS. Powered by Vercel.
                </p>
            </div>
        </footer>
    );
}
