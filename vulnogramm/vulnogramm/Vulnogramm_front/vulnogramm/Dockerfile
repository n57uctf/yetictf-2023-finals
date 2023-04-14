FROM node:18-alpine as react_build

WORKDIR /frontend
COPY package.json package-lock.json ./

RUN npm install -g npm@9.6.4 && npm install
COPY . .

RUN npm run build

# NGINX BUILD
FROM nginx:1.17.1-alpine
COPY nginx.conf /etc/nginx/nginx.conf

COPY --from=react_build /frontend/build/ /usr/share/nginx/html