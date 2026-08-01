import { CONTACTS } from '@/data/content';

export default function Footer() {
  return (
    <footer className="border-t border-white/10 py-8">
      <div className="section-shell flex flex-col gap-6 text-sm text-white/60 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="font-medium text-white/85">AI Visual Studio</p>
          <p className="mt-1">Premium AI visuals for ads, social and digital products.</p>
        </div>
        <div className="flex flex-wrap gap-5">
          <a href="#works">Works</a>
          <a href="#services">Services</a>
          <a href="#process">Process</a>
          <a href="#about">About</a>
          <a href={CONTACTS.telegram}>Telegram</a>
        </div>
        <p>© {new Date().getFullYear()} AI Visual Studio</p>
      </div>
    </footer>
  );
}
