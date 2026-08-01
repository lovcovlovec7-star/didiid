/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './data/**/*.{js,ts,jsx,tsx,mdx}'
  ],
  theme: {
    extend: {
      colors: {
        background: '#06070b',
        panel: '#11131b',
        accent: '#4c7dff',
        violet: '#8459ff',
        cyan: '#43d7ff'
      },
      boxShadow: {
        glow: '0 0 40px rgba(76, 125, 255, 0.25)',
        card: '0 20px 60px rgba(3, 5, 12, 0.6)'
      },
      backgroundImage: {
        noise: "url('data:image/svg+xml,%3Csvg xmlns=\"http://www.w3.org/2000/svg\" width=\"120\" height=\"120\" viewBox=\"0 0 120 120\"%3E%3Cfilter id=\"n\"%3E%3CfeTurbulence type=\"fractalNoise\" baseFrequency=\"1.35\" numOctaves=\"3\" stitchTiles=\"stitch\"/%3E%3C/filter%3E%3Crect width=\"120\" height=\"120\" filter=\"url(%23n)\" opacity=\"0.22\"/%3E%3C/svg%3E')"
      }
    }
  },
  plugins: []
};
