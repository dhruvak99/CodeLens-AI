import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/features/**/*.{js,ts,jsx,tsx,mdx}"
  ],
  theme: {
    extend: {
      colors: {
        background: "#020617",
        foreground: "#F8FAFC",
        card: "#0F172A",
        border: "#1E293B",
        primary: "#7C3AED",
        secondary: "#06B6D4"
      },
      borderRadius: {
        card: "16px"
      },
      fontFamily: {
        sans: ["var(--font-inter)", "Inter", "sans-serif"],
        mono: ["var(--font-jetbrains-mono)", "JetBrains Mono", "monospace"]
      }
    }
  },
  plugins: [require("tailwindcss-animate")]
};

export default config;
