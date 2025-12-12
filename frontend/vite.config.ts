import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  // Añadimos esta línea para eliminar cualquier ambigüedad
  // y decirle a Vite que la raíz del proyecto es esta carpeta.
  root: './',
})
