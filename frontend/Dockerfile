FROM node:16.4.0-alpine AS stage_build
WORKDIR /app
COPY package.json .
COPY package-lock.json .
RUN npm ci
COPY . .
RUN npm run build

FROM caddy:2.6.4-alpine AS stage_caddy
COPY --from=stage_build /app/dist /srv
COPY Caddyfile /etc/caddy
