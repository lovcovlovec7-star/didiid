'use client';

import { useMemo, useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { filters, works } from '@/data/content';
import PortfolioCard from './PortfolioCard';

export default function Portfolio() {
  const [activeFilter, setActiveFilter] = useState('All');

  const filteredWorks = useMemo(() => {
    if (activeFilter === 'All') return works;
    return works.filter((item) => item.category === activeFilter);
  }, [activeFilter]);

  return (
    <section id="works" className="section-shell pt-24">
      <div className="mb-8 flex flex-col gap-5 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="mb-2 text-sm uppercase tracking-[0.25em] text-white/50">Selected Work</p>
          <h2 className="section-title">Portfolio</h2>
        </div>
        <div className="flex flex-wrap gap-2">
          {filters.map((filter) => (
            <button
              key={filter}
              onClick={() => setActiveFilter(filter)}
              className={`rounded-full px-4 py-2 text-sm transition ${
                activeFilter === filter
                  ? 'bg-white text-black'
                  : 'border border-white/15 bg-white/5 text-white/75 hover:bg-white/10'
              }`}
            >
              {filter}
            </button>
          ))}
        </div>
      </div>

      <motion.div layout className="grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3">
        <AnimatePresence mode="popLayout">
          {filteredWorks.map((item, index) => (
            <PortfolioCard key={item.title} item={item} index={index} />
          ))}
        </AnimatePresence>
      </motion.div>
    </section>
  );
}
