# syntax=docker/dockerfile:1

FROM node:22-alpine AS builder
WORKDIR /app

ARG VITE_API_BASE_URL=http://127.0.0.1:5000/api
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
