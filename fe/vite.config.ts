import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  appType: 'mpa',
  server: {
    port: 5500,
    strictPort: true,
    fs: {
      allow: ['..']
    }
  }
})
