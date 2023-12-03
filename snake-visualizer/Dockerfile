FROM node:16.19.1 AS build

LABEL version="1.0"

WORKDIR /app
COPY . .

RUN npm install
RUN npm link typescript

RUN npm run build

FROM nginx:alpine
WORKDIR /usr/share/nginx/html
RUN rm -rf ./*
COPY --from=build /app/dist .
ENTRYPOINT ["nginx", "-g", "daemon off;"]