# neptune

neptune is a dependency & vulnerability inventory for containers. 

Its purpose is to be called during a CI workflow where a container image is built (and optionnaly pushed to a registry).
It will analyze the languages-specific and distro packages installed, check for vulnerabilities based on thoses, and store this informations server-side.
 Operators can then check their dependencies and vulnerabilities inventory

 
# TL;DR

start neptune on port 5000
```
git clone https://github.com/k0rventen/neptune.git
cd neptune
docker build -t neptune .
docker run -v neptune_data:/app/data -p 5000:5000 neptune
```

scan an image using neptune
```
http post :5000/api/scan image=python:3-slim
# or 
curl -d '{"image":"python:3-slim"}' -H "Content-Type: application/json" -X POST http://localhost:5000
```

then open `http://localhost:5000/` to check the ui.


## technical overview

- api: [fastapi](https://fastapi.tiangolo.com/)
- ui: [vuejs](https://vuejs.org/) + [nuxt](https://nuxtjs.org/)
- package scanning: [syft](https://github.com/anchore/syft)
- vulnerability scanning: [grype](https://github.com/anchore/grype)
- OCI images management: [skopeo](https://github.com/containers/skopeo)
- storage: [sqlite](https://www.sqlite.org/index.html)