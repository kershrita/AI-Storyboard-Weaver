/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        "deep-space": "#1C2526",
        "neon-blue": "#00D4FF",
        "cinematic-gold": "#FFD700",
        "soft-white": "#F5F5F5",
      },
      fontFamily: {
        orbitron: ["Orbitron", "sans-serif"],
        montserrat: ["Montserrat", "sans-serif"],
      },
    },
  },
  plugins: [],
};