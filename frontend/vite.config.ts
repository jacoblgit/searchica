import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: '../backend/dist'
  },
  base: '/dist/'  // This will make Vite generate the correct paths in index.html
})