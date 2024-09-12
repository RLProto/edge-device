FROM node:18 as build-stage

WORKDIR /app

RUN npm set strict-ssl false

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

FROM nginx:alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/nginx.conf

COPY --from=build-stage /app/dist /usr/share/nginx/html

COPY --from=build-stage /app/src /usr/share/nginx/html/src

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
