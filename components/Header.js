'use client';

import { Menu, X } from 'lucide-react';
import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const navItems = ['Works', 'Services', 'Process', 'About', 'Contact'];

export default function Header() {
  const [open, setOpen] = useState(false);

  return (
    <header className="fixed inset-x-0 top-0 z-40 border-b border-white/10 bg-black/35 backdrop-blur-xl">
      <div className="section-shell flex h-16 items-center justify-between">
        <a href="#hero" className="text-sm font-semibold uppercase tracking-[0.22em] text-white/90">
          AI Visual Studio
        </a>

        <nav className="hidden items-center gap-8 md:flex">
          {navItems.map((item) => (
            <a key={item} href={`#${item.toLowerCase()}`} className="text-sm text-white/70 transition hover:text-white">
              {item}
            </a>
          ))}
        </nav>

        <button
          onClick={() => setOpen((value) => !value)}
          className="inline-flex rounded-xl border border-white/15 p-2 text-white/80 md:hidden"
          aria-label="Toggle menu"
        >
          {open ? <X size={18} /> : <Menu size={18} />}
        </button>
      </div>

      <AnimatePresence>
        {open ? (
          <motion.nav
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="section-shell overflow-hidden border-t border-white/10 md:hidden"
          >
            <div className="flex flex-col py-4">
              {navItems.map((item) => (
                <a
                  key={item}
                  href={`#${item.toLowerCase()}`}
                  onClick={() => setOpen(false)}
                  className="rounded-lg px-2 py-3 text-white/75 transition hover:bg-white/5 hover:text-white"
                >
                  {item}
                </a>
              ))}
            </div>
          </motion.nav>
        ) : null}
      </AnimatePresence>
    </header>
  );
}
