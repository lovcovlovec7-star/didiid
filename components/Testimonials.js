import { testimonials } from '@/data/content';

export default function Testimonials() {
  return (
    <section className="section-shell pt-24">
      <p className="mb-2 text-sm uppercase tracking-[0.25em] text-white/50">Feedback</p>
      <h2 className="section-title mb-8">Testimonials</h2>
      <div className="grid gap-4 md:grid-cols-3">
        {testimonials.map((quote) => (
          <article key={quote} className="glass-panel rounded-3xl p-6">
            <p className="text-base text-white/82">“{quote}”</p>
          </article>
        ))}
      </div>
    </section>
  );
}
