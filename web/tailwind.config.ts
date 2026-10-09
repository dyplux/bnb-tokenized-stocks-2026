import type { Config } from "tailwindcss";
export default {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "rgb(var(--c-bg) / <alpha-value>)",
        slate: "rgb(var(--c-surface) / <alpha-value>)",
        slate2: "rgb(var(--c-surface2) / <alpha-value>)",
        line: "var(--line)", line2: "var(--line2)",
        fg: "rgb(var(--c-fg) / <alpha-value>)",
        fg2: "rgb(var(--c-fg2) / <alpha-value>)",
        fg3: "rgb(var(--c-fg3) / <alpha-value>)",
        gold: "#FFCC00",                                   // fills: buttons, bars — constant
        goldtext: "rgb(var(--c-goldtext) / <alpha-value>)", // gold used AS TEXT — darkens on light
        golddim: "#C68F0D", up: "#12C77A", down: "#E5484D",
      },
      fontFamily: {
        display: ["var(--font-display)", "system-ui", "sans-serif"],
        sans: ["var(--font-sans)", "system-ui", "sans-serif"],
        mono: ["var(--font-mono)", "ui-monospace", "Menlo", "monospace"],
      },
      maxWidth: { site: "1200px" },
    },
  },
  plugins: [],
} satisfies Config;
