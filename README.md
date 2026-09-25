# West Africa Capitals Quiz

**[Play the live quiz](https://west-africa-quiz.orangetree-477f51ac.uksouth.azurecontainerapps.io)**

A Python web app about the capitals of 16 West African countries. Each round asks about every country once, ends after 16 answers, and shows your final score. It serves a responsive quiz, checks answers through a JSON API, and explains two commonly confused capitals. No Python packages are required.

## Run locally

On a Mac, open Terminal in this folder and run:

```bash
python3 app.py
```

Open http://localhost:8000. Press Control-C to stop. To choose another port: `PORT=8080 python3 app.py`.

## Run with Docker

```bash
docker build -t west-africa-quiz .
docker run --rm -p 8000:8000 west-africa-quiz
```

Open http://localhost:8000. The health endpoint is `/health`.

## Project documentation

Read the [build and deployment record](docs/PROJECT.md) for the architecture, verification steps, Azure resources, and problems solved.

## Azure deployment

The live quiz runs on **Azure Container Apps** (Consumption) in UK South. Its image is stored in **Azure Container Registry** as `oluwestafricaquiz.azurecr.io/west-africa-quiz:v1`. Public HTTP ingress routes to container port **8000**. The application provides a health endpoint at `/health`.

To publish a code change, pull the latest version, rebuild, tag, and push a new image:

```bash
git pull
docker build -t west-africa-quiz .
docker tag west-africa-quiz:latest oluwestafricaquiz.azurecr.io/west-africa-quiz:v2
docker push oluwestafricaquiz.azurecr.io/west-africa-quiz:v2
```

Sign in to the registry before pushing. Then update the Container App's image tag to `v2` in Azure. A new tag makes it clear which version is deployed. The Container App should use managed identity with permission to pull images from the registry. Azure Container Registry can incur ongoing charges, and Container Apps usage beyond its free allowance can incur charges.

## Repository

Source code: [olumideakinseye77-glitch/Olu](https://github.com/olumideakinseye77-glitch/Olu). The app uses Python's standard library and needs no Python dependencies.

## How it works

`GET /api/countries` lists the 16 countries. The browser shuffles that list and requests each country once using `GET /api/question?country=...`. `POST /api/answer` checks a country and selected capital and returns the answer and a brief fact. The browser tracks the score for the current round. There is no database or account. The server uses Python's standard library and the Docker image runs as a non-root user.

## Portfolio talking points

Explain HTTP routes, JSON requests, Docker image layers, the exposed port, Azure container deployment, and why `/health` helps monitor the app. An extension would add GitHub Actions tests and automatic deployment after the first manual deployment works.
