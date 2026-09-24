# West Africa Capitals Quiz

A Python web app about the capitals of 16 West African countries. It serves a responsive quiz, checks answers through a JSON API, and explains two commonly confused capitals. No Python packages are required.

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

## Put it on GitHub

Create an empty repository named `west-africa-quiz` in your GitHub account. From this directory:

```bash
git init
git add .
git commit -m "Build West Africa capitals quiz"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/west-africa-quiz.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username. If Git asks for authentication, use your normal GitHub sign-in flow; never commit credentials.

## Deploy to Azure App Service

Create an Azure App Service **Web App for Containers** running Linux, with an Azure Container Registry image of this project. Set the App Service application setting `WEBSITES_PORT=8000` and use port 8000 for the container. Build and push the image to your registry, then configure the Web App's container image and restart it. The `/health` endpoint returns `{"status": "ok"}`. Registry and App Service usage may incur charges; stop or delete resources when finished.

## How it works

`GET /api/question` returns a country and four choices; `POST /api/answer` checks a country and selected capital and returns the answer and a brief fact. The browser tracks score for the current page session. There is no database or account. Questions may repeat; this is a practice quiz rather than an exam. The server uses Python's standard library and the Docker image runs as a non-root user.

## Portfolio talking points

Explain HTTP routes, JSON requests, Docker image layers, the exposed port, Azure container deployment, and why `/health` helps monitor the app. An extension would add GitHub Actions tests and automatic deployment after the first manual deployment works.
