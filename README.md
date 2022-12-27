# neptune

![Docker Image Size (latest by date)](https://img.shields.io/docker/image-size/k0rventen/neptune)

![header](header.png)
neptune is a dependency & vulnerability inventory for containers. 

It is SBOM driven, and doesn't rely solely on the scan of an image to determine vulnerabilites.
It will analyze the languages-specific and distro packages installed, check for vulnerabilities based on thoses, and store all of theses informations server-side.
That means if a new vulnerability shows up, you don't have to scan your entire inventory again. neptune will automatically link new vulnerabilities to previously scanned images.


Scans can be made through its UI, but it was initially designed to be called during a CI workflow where a container image is built (and optionnaly pushed to a registry).
Operators can then check their dependencies and vulnerabilities inventory through the UI or the API.


## TL;DR

start neptune on port 5000
```
docker run -p 5000:5000 k0rventen/neptune
```

let neptune scan itself
```
# httpie
http post :5000/api/scan image=k0rventen/neptune
# new curl
curl --json '{"image":"k0rventen/neptune"}' http://localhost:5000
# old curl
curl -d '{"image":"k0rventen/neptune"}' -H "Content-Type: application/json" -X POST http://localhost:5000
```

then open `http://localhost:5000/` to check the ui.


## technical overview

- api: [fastapi](https://fastapi.tiangolo.com/)
- ui: [vuejs](https://vuejs.org/) + [nuxt](https://nuxtjs.org/)
- package scanning: [syft](https://github.com/anchore/syft)
- vulnerability scanning: [grype](https://github.com/anchore/grype)
- OCI images management: [skopeo](https://github.com/containers/skopeo)
- storage: [sqlite](https://www.sqlite.org/index.html)
- logo: [craiyon.com](https://www.craiyon.com/)

## API

The OpenAPI documentation is available at `/api` on a running neptune instance. 


## Usage in a CI workflow


Example CI stage in a `.gitlab-ci.yml`:
```yaml
neptune:
  image: alpine:3.16
  before_script:
    - apk add curl
  script:
    - CI_IMAGE="$CI_REGISTRY_IMAGE:${CI_COMMIT_TAG:-latest}"
    - curl --fail-with-body --json '{"image":"'$CI_IMAGE'"}' https://neptune/api/scan
```

## Roadmap

- proper UI
- authentification
- schedules for fetching images
