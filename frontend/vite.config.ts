import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

const port = parseInt(process.env.PORT || '5173', 10)
const apiBase = process.env.VITE_API_BASE_URL || 'http://localhost:8001'

export default defineConfig({
  plugins: [vue(), tailwindcss()],
  server: {
    port,
    proxy: {
      '/api': { target: apiBase, changeOrigin: true }
    }
  }
})
