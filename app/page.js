import Header from '@/components/Header';
import Hero from '@/components/Hero';
import Portfolio from '@/components/Portfolio';
import Services from '@/components/Services';
import Process from '@/components/Process';
import About from '@/components/About';
import Testimonials from '@/components/Testimonials';
import Contact from '@/components/Contact';
import Footer from '@/components/Footer';

export default function HomePage() {
  return (
    <main>
      <Header />
      <Hero />
      <Portfolio />
      <Services />
      <Process />
      <About />
      <Testimonials />
      <Contact />
      <Footer />
    </main>
  );
}
