'use client';

import { motion } from 'framer-motion';
import { services } from '@/data/content';

export default function Services() {
  return (
    <section id="services" className="section-shell pt-24">
      <p className="mb-2 text-sm uppercase tracking-[0.25em] text-white/50">What I do</p>
      <h2 className="section-title mb-8">Services</h2>
      <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
        {services.map((service, index) => {
          const Icon = service.icon;
          return (
            <motion.article
              key={service.title}
              initial={{ y: 24, opacity: 0 }}
              whileInView={{ y: 0, opacity: 1 }}
              viewport={{ once: true, amount: 0.3 }}
              transition={{ delay: index * 0.06, duration: 0.4 }}
              className="glass-panel rounded-3xl p-6 transition hover:border-cyan/40 hover:bg-white/[0.07]"
            >
              <Icon className="mb-4 text-cyan" />
              <h3 className="text-xl font-medium">{service.title}</h3>
              <p className="mt-3 text-sm text-white/70">{service.description}</p>
              <ul className="mt-4 space-y-2 text-sm text-white/75">
                {service.outcomes.map((item) => (
                  <li key={item} className="flex items-start gap-2">
                    <span className="mt-1 h-1.5 w-1.5 rounded-full bg-cyan/80" />
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </motion.article>
          );
        })}
      </div>
    </section>
  );
}
