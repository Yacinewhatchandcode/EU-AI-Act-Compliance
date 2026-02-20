import { promises as fs } from 'fs';
import path from 'path';
import Link from 'next/link';
import Header from './components/Header';
import Footer from './components/Footer';

// Define the News Item type
type NewsItem = {
  id: number;
  title: string;
  date: string;
  category: string;
  summary: string;
  content: string;
  source: string;
  link?: string;
  tags?: string[];
};

async function getNews() {
  const filePath = path.join(process.cwd(), 'public/data/news.json');
  try {
    const fileContents = await fs.readFile(filePath, 'utf8');
    return JSON.parse(fileContents) as NewsItem[];
  } catch (error) {
    console.error("News file not found or empty", error);
    return [];
  }
}

export default async function Home() {
  const news = await getNews();
  const featured = news[0]; // The latest news is featured
  const rest = news.slice(1);

  return (
    <main className="flex flex-col min-h-screen bg-slate-900 text-slate-100">
      <Header />

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 px-4 sm:px-6 lg:px-8 overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-full bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-800 via-slate-900 to-slate-950 z-0"></div>
        <div className="relative z-10 max-w-7xl mx-auto text-center">
          <h1 className="text-5xl md:text-7xl font-display font-bold mb-6 tracking-tight bg-clip-text text-transparent bg-gradient-to-b from-white to-slate-400">
            The Algorithmic <br />
            <span className="text-yellow-500">Journal</span>
          </h1>
          <p className="text-xl md:text-2xl text-slate-400 max-w-3xl mx-auto mb-10 leading-relaxed">
            Cutting-edge insights on the <strong className="text-white">European AI Act 2026</strong> and the ethical frontier of autonomous systems.
          </p>
          <div className="flex justify-center gap-4">
            <Link href="#latest" className="px-8 py-3 bg-white/10 hover:bg-white/20 backdrop-filter backdrop-blur-sm border border-white/20 rounded-full text-white font-medium transition-all group">
              Latest Updates <span className="inline-block transition-transform group-hover:translate-y-1">↓</span>
            </Link>
          </div>
        </div>
      </section>

      {/* Featured Article */}
      {featured && (
        <section className="py-12 bg-slate-950 border-y border-white/5">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid md:grid-cols-2 gap-12 items-center">
              <div className="order-2 md:order-1 space-y-6">
                <span className="inline-block px-3 py-1 bg-yellow-500/10 text-yellow-500 text-xs font-bold tracking-wider uppercase rounded-full border border-yellow-500/20">
                  {featured.category} • Featured
                </span>
                <h2 className="text-3xl md:text-4xl font-display font-bold leading-tight text-white">
                  {featured.title}
                </h2>
                <p className="text-lg text-slate-400 leading-relaxed">
                  {featured.summary}
                </p>
                <div className="pt-4 flex items-center gap-4 text-sm text-slate-500">
                  <span>{new Date(featured.date).toLocaleDateString()}</span>
                  <span>•</span>
                  <span>{featured.source}</span>
                </div>
              </div>
              <div className="order-1 md:order-2 relative aspect-video bg-gradient-to-tr from-slate-800 to-slate-700 rounded-2xl overflow-hidden shadow-2xl border border-white/10 flex items-center justify-center group">
                <div className="absolute inset-0 bg-yellow-500/5 group-hover:bg-yellow-500/10 transition-colors duration-500"></div>
                <div className="text-9xl text-white/5 font-display font-bold select-none group-hover:scale-110 transition-transform duration-700">AI</div>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* News Grid */}
      <section id="latest" className="py-20 bg-slate-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between mb-12">
            <h3 className="text-2xl font-display font-bold text-white">Latest Analysis</h3>
            <div className="h-px bg-white/10 flex-grow ml-8"></div>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {rest.map((item) => (
              <article key={item.id} className="group flex flex-col h-full bg-slate-800/30 border border-white/5 rounded-xl overflow-hidden hover:border-yellow-500/30 hover:bg-slate-800/50 transition-all duration-300 hover:-translate-y-1 hover:shadow-xl hover:shadow-yellow-900/5">
                <div className="p-8 flex flex-col h-full">
                  <div className="flex justify-between items-start mb-4">
                    <span className="text-xs font-bold text-yellow-500 uppercase tracking-wider">{item.category}</span>
                    <span className="text-xs text-slate-500">{new Date(item.date).toLocaleDateString()}</span>
                  </div>
                  <h4 className="text-xl font-display font-bold mb-3 text-slate-100 group-hover:text-yellow-400 transition-colors">
                    <Link href={item.link || "#"} target="_blank" className="hover:underline decoration-yellow-500/30 underline-offset-4">
                      {item.title}
                    </Link>
                  </h4>
                  <p className="text-slate-400 text-sm leading-relaxed mb-6 flex-grow line-clamp-4">
                    {item.summary}
                  </p>
                  <div className="pt-4 border-t border-white/5 flex items-center justify-between mt-auto">
                    <span className="text-xs text-slate-500 font-medium">{item.source}</span>
                    {item.link && (
                      <Link href={item.link} target="_blank" className="text-xs text-yellow-500 hover:text-white transition-colors flex items-center gap-1">
                        Read Source →
                      </Link>
                    )}
                  </div>
                </div>
              </article>
            ))}
          </div>
        </div>
      </section>

      <Footer />
    </main>
  );
}
