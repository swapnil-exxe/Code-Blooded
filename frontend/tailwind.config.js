/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        serif: ['Lora', 'Georgia', 'serif'],
        sans: ['"Plus Jakarta Sans"', 'system-ui', 'sans-serif'],
      },
      colors: {
        ivory: {
          50: '#FDFBF7',
          100: '#FAF8F5',
          200: '#F4EFE6',
          300: '#EAE3D2',
        },
        institutional: {
          50: '#F0F7F4',
          100: '#DDEFE8',
          700: '#134E4A',
          800: '#0F382C',
          900: '#0A2920',
        },
        terracotta: {
          500: '#D97706',
          600: '#C25E00',
          700: '#9A4A00',
        },
        gov: {
          navy: '#0b192c',
          deep: '#0c1b2e',
          slate: '#0f172a',
          blue: '#1e3a8a',
          interactive: '#1d4ed8',
          surface: '#f8fafc',
          card: '#ffffff',
          border: '#e2e8f0',
          subtle: '#f1f5f9',
        },
        saffron: {
          50: '#fffbeb',
          100: '#fef3c7',
          500: '#f59e0b',
          600: '#d97706',
          700: '#b45309',
        }
      }
    },
  },
  plugins: [],
}

