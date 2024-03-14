# binary fetch layer
FROM debian:bullseye as bin-downloader
RUN apt update && apt install upx-ucl curl ca-certificates -y --no-install-recommends
WORKDIR /download
ARG SYFT_VERSION=v0.96.0
ARG GRYPE_VERSION=v0.73.1
RUN curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b . ${SYFT_VERSION}
RUN curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b . ${GRYPE_VERSION}
RUN upx grype syft


# backend build layer
FROM python:3.12-alpine as backend-builder
RUN apk add build-base
COPY backend/requirements.txt .
RUN pip3 install --prefix="/install" -r requirements.txt


# frontend build layer
FROM node:18-alpine as frontend-build
RUN apk add git
WORKDIR /app
COPY front/package.json ./
RUN npm install 
COPY front ./
RUN npx nuxi generate


# final layer
FROM python:3.12-alpine
# copy runtime libs, deps and binaries from other layers
RUN apk add skopeo
COPY --from=backend-builder /install /usr/local/
COPY --from=bin-downloader /download /usr/local/bin
# preload the CVE db
ENV GRYPE_DB_CACHE_DIR /app/data/grype
RUN grype db update
# add back/front end code
WORKDIR /app/src
COPY backend/src/ .
COPY --from=frontend-build /app/.output/public/ /app/dist/

# start neptune
ENTRYPOINT python3 -u app.py