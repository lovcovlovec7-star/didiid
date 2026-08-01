'use client';

import { motion } from 'framer-motion';
import MediaBlock from './MediaBlock';

export default function PortfolioCard({ item, index }) {
  const isWide = index % 5 === 0;

  return (
    <motion.article
      layout
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 14 }}
      transition={{ duration: 0.35 }}
      className={`group glass-panel overflow-hidden rounded-3xl shadow-card transition duration-300 hover:-translate-y-1 hover:shadow-glow ${
        isWide ? 'md:col-span-2 lg:col-span-2' : ''
      }`}
    >
      <div className="relative h-64 w-full sm:h-72">
        <MediaBlock src={item.src} type={item.type} fallbackTitle={item.title} />
      </div>
      <div className="space-y-3 p-5">
        <p className="text-xs uppercase tracking-[0.18em] text-cyan/80">{item.category}</p>
        <h3 className="text-xl font-medium text-white">{item.title}</h3>
        <p className="text-sm text-white/65">{item.description}</p>
        <div className="flex flex-wrap gap-2 pt-1">
          {item.tags.map((tag) => (
            <span key={tag} className="rounded-full bg-white/6 px-2.5 py-1 text-xs text-white/70">
              {tag}
            </span>
          ))}
        </div>
      </div>
    </motion.article>
  );
}
