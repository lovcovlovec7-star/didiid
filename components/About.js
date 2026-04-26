import { stats } from '@/data/content';

export default function About() {
  return (
    <section id="about" className="section-shell pt-24">
      <div className="grid gap-8 lg:grid-cols-[1.2fr_1fr]">
        <div>
          <p className="mb-2 text-sm uppercase tracking-[0.25em] text-white/50">About</p>
          <h2 className="section-title mb-4">Commercial visual storytelling with AI</h2>
          <p className="max-w-2xl text-white/72">
            I help brands and creators turn ideas into cinematic AI visuals. My focus is not just generation, but
            commercial impact: strong hooks, clean composition, premium style and content that works on social media.
          </p>
        </div>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          {stats.map((item) => (
            <article key={item.label} className="glass-panel rounded-2xl p-5">
              <p className="text-2xl font-semibold text-cyan">{item.value}</p>
              <p className="mt-2 text-sm text-white/70">{item.label}</p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
