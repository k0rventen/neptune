# binary fetch layer
FROM debian as bin-downloader
RUN apt update && apt install upx-ucl wget ca-certificates -y --no-install-recommends
WORKDIR /download
RUN wget https://github.com/anchore/grype/releases/download/v0.50.2/grype_0.50.2_linux_amd64.tar.gz -O grype.tar.gz
RUN wget https://github.com/anchore/syft/releases/download/v0.57.0/syft_0.57.0_linux_amd64.tar.gz -O syft.tar.gz
RUN mkdir -p bin/
RUN tar xvf grype.tar.gz grype
RUN tar xvf syft.tar.gz syft
RUN upx grype syft
RUN mv grype syft bin/

# backend build layer
FROM python:3.10-alpine as backend-builder
RUN apk add build-base
COPY requirements.txt .
RUN pip3 install  --prefix="/install" -r requirements.txt


# final layer
FROM python:3.10-alpine
RUN apk add skopeo
COPY --from=backend-builder /install /usr/local/
COPY --from=bin-downloader /download/bin /usr/local/bin
WORKDIR /app
COPY src/ ./
RUN mkdir dist

ENV PYTHONUNBUFFERED 1
ENTRYPOINT ["python3","app.py"]