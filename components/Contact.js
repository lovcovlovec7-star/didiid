'use client';

import { useState } from 'react';
import { CONTACTS } from '@/data/content';

export default function Contact() {
  const [notice, setNotice] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    setNotice('Thanks! Please contact me directly via Telegram or email.');
  };

  return (
    <section id="contact" className="section-shell pb-20 pt-24">
      <div className="glass-panel rounded-3xl p-6 sm:p-10">
        <h2 className="max-w-2xl text-3xl font-semibold leading-tight sm:text-4xl">
          Let’s create something that people will stop scrolling for.
        </h2>
        <p className="mt-4 max-w-2xl text-white/72">
          Send me your idea, product, references or raw materials — I’ll turn it into a visual concept.
        </p>

        <div className="mt-6 flex flex-wrap gap-3">
          <a href={CONTACTS.telegram} target="_blank" rel="noreferrer" className="rounded-xl bg-white px-5 py-3 text-sm font-medium text-black">
            Contact on Telegram
          </a>
          <a href={CONTACTS.email} className="rounded-xl border border-white/20 px-5 py-3 text-sm font-medium text-white hover:bg-white/10">
            Send an email
          </a>
        </div>

        <form onSubmit={handleSubmit} className="mt-8 grid gap-4 sm:grid-cols-2">
          <input required placeholder="Name" className="rounded-xl border border-white/15 bg-black/40 px-4 py-3 text-sm outline-none focus:border-cyan" />
          <input required placeholder="Project type" className="rounded-xl border border-white/15 bg-black/40 px-4 py-3 text-sm outline-none focus:border-cyan" />
          <textarea required placeholder="Message" className="min-h-32 rounded-xl border border-white/15 bg-black/40 px-4 py-3 text-sm outline-none focus:border-cyan sm:col-span-2" />
          <button type="submit" className="w-fit rounded-xl bg-cyan px-5 py-3 text-sm font-medium text-black">
            Send request
          </button>
        </form>

        {notice ? <p className="mt-4 rounded-xl border border-cyan/40 bg-cyan/10 p-3 text-sm text-cyan">{notice}</p> : null}
      </div>
    </section>
  );
}
