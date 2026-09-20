import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["'Space Grotesk'", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "sans-serif"],
      },
      colors: {
        background: "#0D0E11",
        foreground: "#F3F4F6",
        surface: "#161920",
        "surface-hover": "#20242d",
        card: "#161920",
        "card-border": "#2b303a",
        "border-light": "#3b424e",
        primary: {
          DEFAULT: "#C5FF45",
          hover: "#b1eb2f",
          light: "#dcff8c",
          subtle: "rgba(197, 255, 69, 0.16)",
        },
        secondary: {
          DEFAULT: "#111318",
          hover: "#20242d",
        },
        danger: {
          DEFAULT: "#FF6B00",
          hover: "#e85f00",
        },
        success: "#C5FF45",
        warning: "#FF6B00",
        muted: "#6b7280",
      },
      borderRadius: {
        DEFAULT: "6px",
        md: "8px",
        lg: "12px",
      },
    },
  },
  plugins: [],
};
export default config;