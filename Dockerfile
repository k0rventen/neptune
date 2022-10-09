# binary fetch layer
FROM debian as bin-downloader
RUN apt update && apt install upx-ucl wget ca-certificates -y --no-install-recommends
WORKDIR /download
ARG SYFT_VERSION=0.58.0
ARG GRYPE_VERSION=0.50.2
RUN wget https://github.com/anchore/grype/releases/download/v${GRYPE_VERSION}/grype_${GRYPE_VERSION}_linux_amd64.tar.gz -qO - | tar xz
RUN wget https://github.com/anchore/syft/releases/download/v${SYFT_VERSION}/syft_${SYFT_VERSION}_linux_amd64.tar.gz -qO - | tar xz
RUN upx grype syft

# backend build layer
FROM python:3.10-alpine as backend-builder
RUN apk add build-base
COPY backend/requirements.txt .
RUN pip3 install --prefix="/install" -r requirements.txt

# frontend build layer
FROM node:lts-alpine as frontend-build
RUN apk add git
WORKDIR /app
COPY frontend/package.json ./
RUN yarn install --progress=false
COPY . .
RUN yarn run generate

# final layer
FROM python:3.10-alpine
RUN apk add skopeo
COPY --from=backend-builder /install /usr/local/
COPY --from=bin-downloader /download /usr/local/bin
WORKDIR /app
COPY backend/src/ ./
COPY --from=frontend-build /app/dist dist/

ENV PYTHONUNBUFFERED 1
ENTRYPOINT ["python3","app.py"]