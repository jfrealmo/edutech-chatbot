# 📘 Edutech ChatBot — Guía de instalación y ejecución

Este proyecto implementa un asistente educativo con frontend en **React/Vite/TypeScript** y backend en **Python/FastAPI**, desplegado mediante **Docker** y **Nginx** para producción.

---

## 🚀 Requisitos previos: (instalar)

- [Docker](https://docs.docker.com/get-docker/),  [Docker Compose](https://docs.docker.com/compose/) y
[ollama](https://ollama.com/);
 una vez instalados, asegúrate de que Docker desktop esté corriendo antes de ejecutar los comandos.
- Git para clonar el repositorio:

1. Ejecutar en la terminal de comandos:
  git clone https://github.com/jfrealmo/edutech-chatbot
  cd chatbot_hackaton

2. Levantar el entorno, ejecutando en la terminal:
docker compose -f docker-compose.prod.yml up -d

3. 🌐 Abrir el navegador en:
- Frontend → http://localhost
- Backend → http://localhost:8000

Para usar el chatbot con IA se debe tener en cuenta:

1. Si se tiene código (con créditos) de proveedor de pago como OPENAI, CLAUDE u otro.  La aplicación se conectará directamente al proveedor de pago.

2. Si no se tiene código, se debe abrir Ollama en la terminal de comandos CMD: y ejecutar: ollama run llama2, luego escribir p. ej: "Hola" y mantener abierta la ventana del CMD, mientras se usa el chatbot.

***Estos fueron los pasos que se siguieron para pasar a la arquitectura contenerizada con Docker (no hay que volver a realizar)***


🛠️ Entorno de desarrollo,
Se trabajó en modo desarrollo con hot reload, ejecuta en la terminal de comandos:

npm install
npm run dev

Esto levantantando el frontend en http://localhost:5173 y el backend en http://localhost:8000.

🛠️ Entorno de producción con Docker:

npm install
npm run build

1. Se consruyeron imágenes, ejecutando en la terminal de comandos:

docker compose -f docker-compose.prod.yml build

2. Se hizo levantamiento de contenedores, ejecutando en la terminal de comandos:

docker compose -f docker-compose.prod.yml up -d

3. Se hizo verificación de contenedores, ejecutando en la terminal de comandos:

docker compose -f docker-compose.prod.yml ps

Ejemplo de salida en consola:

NAME                    IMAGE                       STATUS              PORTS
chatbot_backend_prod    chatbot_hackaton-backend    Up                  0.0.0.0:8000->8000/tcp
chatbot_frontend_prod   chatbot_hackaton-frontend   Up                  0.0.0.0:80->80/tcp


🌐 Acceso a la aplicación
- Frontend (Nginx) → http://localhost
- Backend (FastAPI/Node) → http://localhost:8000
👉 Las llamadas desde el frontend a /api se redirigen automáticamente al backend gracias a la configuración de Nginx.

📂 Estructura relevante:

frontend/
  Dockerfile          # Multi-etapa: build + Nginx
  nginx.conf          # Configuración de proxy /api → backend
  vite.config.ts      # Proxy para desarrollo local
docker-compose.prod.yml

🧰 Comandos útiles
- Ver logs:

docker logs chatbot_frontend_prod
docker logs chatbot_backend_prod

- Detener contenedores:

docker compose -f docker-compose.prod.yml down

- Reconstruir imágenes:

docker compose -f docker-compose.prod.yml build --no-cache

