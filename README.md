# Olu's Azure DevOps Portfolio

## Project 1 — West Africa Capitals Quiz

**Status: Complete · [Play the live quiz](https://west-africa-quiz.orangetree-477f51ac.uksouth.azurecontainerapps.io) · [Read the project write-up](docs/PROJECT.md)**

A Python web app about the capitals of 16 West African countries. Each round asks about every country once, ends after 16 answers, and shows your final score. It serves a responsive quiz, checks answers through a JSON API, and explains two commonly confused capitals. No Python packages are required.

### Run locally

On a Mac, open Terminal in this folder and run:

```bash
python3 app.py
```

Open http://localhost:8000. Press Control-C to stop. To choose another port: `PORT=8080 python3 app.py`.

### Run with Docker

```bash
docker build -t west-africa-quiz .
docker run --rm -p 8000:8000 west-africa-quiz
```

Open http://localhost:8000. The health endpoint is `/health`.

### Project documentation

Read the [build and deployment record](docs/PROJECT.md) for the architecture, verification steps, Azure resources, and problems solved.

### Azure deployment

The live quiz runs on **Azure Container Apps** (Consumption) in UK South. Its image is stored in **Azure Container Registry** as `oluwestafricaquiz.azurecr.io/west-africa-quiz:v1`. Public HTTP ingress routes to container port **8000**. The application provides a health endpoint at `/health`.

To publish a code change, pull the latest version, rebuild, tag, and push a new image:

```bash
git pull
docker build -t west-africa-quiz .
docker tag west-africa-quiz:latest oluwestafricaquiz.azurecr.io/west-africa-quiz:v2
docker push oluwestafricaquiz.azurecr.io/west-africa-quiz:v2
```

Sign in to the registry before pushing. Then update the Container App's image tag to `v2` in Azure. A new tag makes it clear which version is deployed. The Container App should use managed identity with permission to pull images from the registry. Azure Container Registry can incur ongoing charges, and Container Apps usage beyond its free allowance can incur charges.

### Repository

Source code: [olumideakinseye77-glitch/Olu](https://github.com/olumideakinseye77-glitch/Olu). The app uses Python's standard library and needs no Python dependencies.

### How it works

`GET /api/countries` lists the 16 countries. The browser shuffles that list and requests each country once using `GET /api/question?country=...`. `POST /api/answer` checks a country and selected capital and returns the answer and a brief fact. The browser tracks the score for the current round. There is no database or account. The server uses Python's standard library and the Docker image runs as a non-root user.

### Portfolio talking points

Explain HTTP routes, JSON requests, Docker image layers, the exposed port, Azure container deployment, and why `/health` helps monitor the app. An extension would add GitHub Actions tests and automatic deployment after the first manual deployment works.

## Project 2 — Terraform Staging Deployment on Azure

**Status: Deployed and verified · [Play the staging quiz](https://west-africa-quiz-staging.orangetree-477f51ac.uksouth.azurecontainerapps.io) · [Review the Terraform code and deployment record](https://github.com/olumideakinseye77-glitch/Olu/pull/1)**

I used **Terraform** to deploy a separate staging copy of my West Africa Capitals Quiz. It runs on Azure Container Apps in UK South using the existing Docker image in Azure Container Registry. The production quiz from Project 1 continues to run separately.

### What I built

- Terraform reads the existing resource group, Container Apps environment, and container registry.
- It creates a staging Container App, a user-assigned managed identity, and a registry-scoped `AcrPull` role assignment. The app has public HTTPS ingress on port 8000 and can scale from zero to one replica.
- Terraform state is held in a private Azure Storage blob container, so the deployment can be managed across temporary Azure Cloud Shell sessions. The provider lock file pins the tested AzureRM provider version.

### What I verified

I ran `terraform fmt`, `terraform validate`, and reviewed a plan showing **3 to add, 0 to change, 0 to destroy**. The apply created those three resources. I played the staging quiz in a browser, then ran another plan that reported **No changes**. The production app was not included in the changes.

### Problems I solved

Cloud Shell initially could not get a storage token, and Terraform received a `403` when accessing the state container. I signed in to the correct Azure tenant and granted my user **Storage Blob Data Contributor** on the state storage account. After deployment, Azure reported the default `Consumption` workload profile, which produced a one-line Terraform difference. I declared that profile explicitly and confirmed a clean plan.

### Why this matters

This project shows I can describe Azure infrastructure as code, control access with managed identity and role assignments, keep Terraform state durable, and verify that the deployed resources match the configuration. These are practical skills for **junior Azure cloud engineering and DevOps roles**. A hiring manager can inspect the [Terraform files and full setup guide](https://github.com/olumideakinseye77-glitch/Olu/tree/project-2-terraform-staging/infra) and try both the [production quiz](https://west-africa-quiz.orangetree-477f51ac.uksouth.azurecontainerapps.io) and [staging quiz](https://west-africa-quiz-staging.orangetree-477f51ac.uksouth.azurecontainerapps.io).

**Next:** Project 3 will add automated tests and a GitHub Actions build and deployment workflow.
