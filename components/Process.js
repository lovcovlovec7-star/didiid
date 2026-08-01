'use client';

import { motion } from 'framer-motion';
import { processSteps } from '@/data/content';

export default function Process() {
  return (
    <section id="process" className="section-shell pt-24">
      <p className="mb-2 text-sm uppercase tracking-[0.25em] text-white/50">Workflow</p>
      <h2 className="section-title mb-8">Process</h2>
      <div className="relative grid gap-6 md:grid-cols-4 md:gap-4">
        <div className="absolute left-0 right-0 top-8 hidden h-px bg-gradient-to-r from-transparent via-white/20 to-transparent md:block" />
        {processSteps.map((step, idx) => (
          <motion.article
            key={step.title}
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.5 }}
            transition={{ duration: 0.35, delay: idx * 0.08 }}
            className="glass-panel relative rounded-3xl p-5"
          >
            <p className="mb-3 text-3xl font-semibold text-cyan/90">0{idx + 1}</p>
            <h3 className="mb-2 text-lg font-medium">{step.title}</h3>
            <p className="text-sm text-white/70">{step.description}</p>
          </motion.article>
        ))}
      </div>
    </section>
  );
}
