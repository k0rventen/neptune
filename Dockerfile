# binary fetch layer
FROM debian as bin-downloader
RUN apt update && apt install upx-ucl curl ca-certificates -y --no-install-recommends
WORKDIR /download
ARG SYFT_VERSION=v0.58.0
ARG GRYPE_VERSION=v0.50.2
RUN curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b . ${SYFT_VERSION}
RUN curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b . ${GRYPE_VERSION}
RUN upx grype syft

# backend build layer
FROM python:3.11-alpine as backend-builder
RUN apk add build-base
COPY backend/requirements.txt .
RUN pip3 install --prefix="/install" -r requirements.txt

# frontend build layer
FROM node:16-alpine as frontend-build
RUN apk add git
WORKDIR /app
COPY frontend/package.json ./
RUN yarn install --progress=false
COPY frontend ./
RUN yarn run generate

# final layer
FROM python:3.11-alpine
RUN apk add skopeo
COPY --from=backend-builder /install /usr/local/
COPY --from=bin-downloader /download /usr/local/bin
WORKDIR /app
COPY backend/src/ ./
COPY --from=frontend-build /app/dist dist/

ENV PYTHONUNBUFFERED 1
ENTRYPOINT ["python3","app.py"]