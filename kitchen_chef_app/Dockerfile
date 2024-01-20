FROM node:20.11.0-bullseye AS base

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 5173

####################
# debug
####################

FROM base AS debug

WORKDIR /app
CMD ["npm", "run", "dev-container"]

####################
# build
####################

FROM base AS build

WORKDIR /app

RUN npm run build

####################
# prod
####################

FROM nginx:1.25.0-alpine as prod

WORKDIR /etc/nginx/conf.d

COPY nginx.conf ./
RUN mv nginx.conf default.conf
WORKDIR /usr/share/nginx/html
RUN rm -rf ./*
COPY --from=build /app/dist .
ENTRYPOINT ["nginx", "-g", "daemon off;"]
