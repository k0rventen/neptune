# frontend build layer
FROM node:lts-alpine as frontend-build
RUN apk add git
WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn install  --progress=false
COPY . .
RUN yarn run generate
