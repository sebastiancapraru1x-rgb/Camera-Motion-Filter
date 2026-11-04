# Stage 1: Build React dashboard
FROM node:20-alpine AS frontend
WORKDIR /app/dashboard
COPY dashboard/package.json ./
RUN npm install
COPY dashboard/ ./
RUN npm run build

# Stage 2: Python backend + serve dashboard
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY --from=frontend /app/dashboard/dist ./dashboard/dist
CMD ["uvicorn", "src.api.server:app", "--host", "0.0.0.0", "--port", "8000"]