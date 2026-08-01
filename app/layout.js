import './globals.css';

export const metadata = {
  title: 'AI Visual Studio',
  description: 'Cinematic AI visuals for brands, ads and social media'
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className="scroll-smooth">
      <body className="bg-background text-white antialiased">{children}</body>
    </html>
  );
}
