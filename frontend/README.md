Frontend EduchatBot

Este documento resume la experiencia y configuración necesarias para lograr que la interfaz del asistente educativo se vea correctamente, tal como en la presentación del Hackatón.

📂 Arquitectura del Proyecto

frontend/ → carpeta principal del proyecto React + Vite + Tailwind.

src/

App.tsx → punto de entrada que importa y renderiza EduchatBot.tsx.

EduchatBot.tsx → componente principal que contiene toda la interfaz del asistente.

main.tsx → inicializa React y monta la aplicación.

index.css → incluye las directivas de Tailwind.

index.html → archivo raíz que referencia main.tsx.

tailwind.config.js → configuración de Tailwind.

postcss.config.cjs → configuración de PostCSS.

vite.config.ts → configuración de Vite.

package.json → dependencias y scripts.

⚙️ Configuración Clave

1. Tailwind CSS

El archivo tailwind.config.js debe incluir:

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

👉 Esto asegura que Tailwind escanee todos los archivos .tsx y compile las clases utilizadas.

2. PostCSS

El archivo postcss.config.cjs debe estar en formato CommonJS:

module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}

👉 Si se usa .js en un proyecto con "type": "module", aparecerá el error module is not defined. Por eso debe ser .cjs.

3. App.tsx

Debe apuntar directamente a EduchatBot.tsx:

import EduchatBot from './EduchatBot'

function App() {
  return <EduchatBot />
}

export default App

👉 Esto garantiza que la interfaz completa del asistente se renderice.

4. index.css

Debe contener únicamente:

@tailwind base;
@tailwind components;
@tailwind utilities;

🚀 Scripts de ejecución

Desarrollo:

npm run dev

Levanta el servidor en http://localhost:5173.

Compilación para producción:

npm run build

Genera la carpeta dist/ optimizada.

Previsualización del build:

npm run preview

Sirve la carpeta dist/ para validar la apariencia final.

✅ Conclusión

El problema inicial se debía a configuraciones incompletas o incompatibles:

Falta de tailwind.config.js con rutas correctas.

postcss.config.js mal interpretado como ESM.

App.tsx no apuntaba a EduchatBot.tsx.

Al recrear los archivos con npx tailwindcss init -p y ajustar App.tsx, la interfaz se mostró correctamente con todos los estilos del Hackatón.

📌 Recomendación

Documentar siempre:

La estructura de carpetas.

Los archivos de configuración.

Los pasos de compilación y ejecución.

Esto asegura que cualquier desarrollador pueda replicar la interfaz sin errores.