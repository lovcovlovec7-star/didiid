'use client';

import { motion } from 'framer-motion';
import { useState } from 'react';

export default function Hero() {
  const [videoError, setVideoError] = useState(false);

  return (
    <section id="hero" className="section-shell relative pt-28 sm:pt-32">
      <motion.div
        animate={{ y: [0, -8, 0] }}
        transition={{ duration: 9, repeat: Infinity, ease: 'easeInOut' }}
        className="pointer-events-none absolute -left-20 top-16 h-52 w-52 rounded-full bg-accent/25 blur-[100px]"
      />
      <motion.div
        animate={{ y: [0, 8, 0] }}
        transition={{ duration: 11, repeat: Infinity, ease: 'easeInOut' }}
        className="pointer-events-none absolute -right-16 top-24 h-64 w-64 rounded-full bg-violet/25 blur-[120px]"
      />

      <div className="grid items-center gap-10 lg:grid-cols-[1fr_1.05fr]">
        <div>
          <motion.h1
            initial={{ y: 40, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.7 }}
            className="text-4xl font-semibold leading-tight tracking-tight sm:text-5xl lg:text-6xl"
          >
            Cinematic AI visuals for brands, ads and social media
          </motion.h1>
          <motion.p
            initial={{ y: 28, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.7, delay: 0.15 }}
            className="mt-6 max-w-xl text-base text-white/70 sm:text-lg"
          >
            I create AI-generated videos, product visuals, posters, creative ads and scroll-stopping content for businesses and creators.
          </motion.p>
          <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.7, delay: 0.3 }}
            className="mt-8 flex flex-wrap gap-4"
          >
            <a href="#works" className="rounded-xl bg-white px-6 py-3 text-sm font-medium text-black transition hover:opacity-90">
              View works
            </a>
            <a href="#contact" className="rounded-xl border border-white/20 px-6 py-3 text-sm font-medium text-white transition hover:bg-white/10">
              Contact me
            </a>
          </motion.div>
        </div>

        <motion.div
          animate={{ y: [0, -6, 0] }}
          transition={{ duration: 8, repeat: Infinity, ease: 'easeInOut' }}
          className="glass-panel relative overflow-hidden rounded-3xl p-2 shadow-card"
        >
          <div className="relative aspect-[4/5] overflow-hidden rounded-[1.35rem] bg-gradient-to-br from-[#0f1528] via-[#15182a] to-[#0a0c13]">
            {!videoError ? (
              <video
                autoPlay
                muted
                loop
                playsInline
                preload="metadata"
                poster="/assets/hero-preview.jpg"
                onError={() => setVideoError(true)}
                className="h-full w-full object-cover"
              >
                <source src="/assets/hero-video.mp4" />
              </video>
            ) : (
              <div className="flex h-full w-full items-center justify-center">
                <p className="text-lg text-white/80">Hero video preview</p>
              </div>
            )}
            <div className="absolute inset-0 bg-gradient-to-t from-black/50 via-black/20 to-black/45" />

            <div className="absolute left-4 top-4 flex flex-wrap gap-2">
              {['AI Video', 'Commercial Visuals', 'Product Ads', 'Social Media Content'].map((badge) => (
                <span key={badge} className="rounded-full border border-white/20 bg-black/35 px-3 py-1 text-xs text-white/90 backdrop-blur">
                  {badge}
                </span>
              ))}
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
