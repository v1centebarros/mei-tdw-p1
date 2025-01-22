# Deployment

## How to run

1. Clone the repository

```bash
git clone https://github.com/v1centebarros/mei-tdw-p1.git
```

2. Change to the project directory

```bash
cd mei-tdw-p1/docker
```

3. Run API through docker-compose

It will take a while to download the images and build the containers and then a bit to download the models.

```bash
docker compose up --build -d
```

4. Running frontend

Frontend must be run in dev mode due to the new React compiler which caused many libraries to break namely the ones used in this project for authentication.

First you need to place the .env.local file in the frontend directory with the following content:

```env

AUTH_SECRET="i9SqyC7xA1YFNESd3RVITVUPhY/7yKefr+xBFKiP75M="

AUTH_KEYCLOAK_ID=tdw-client
AUTH_KEYCLOAK_SECRET=WnM69tiQwcscM9Ix0f5TXppHOuS917lm
AUTH_KEYCLOAK_ISSUER=http://localhost:4200/realms/TDW

NODE_ENV=development

NEXT_PUBLIC_API_URL=http://localhost:6969/api

```

```bash
  cd ../frontend
  npm i --legacy-peer-deps
  npm run dev
```

5. Access the frontend in your browser [http://localhost:3000](http://localhost:3000)


## Important notes

1. When uploading the first file it will take some time due to the download of more models.
2. When uploading a file you cannot change page since it will cancel the upload.

## How to stop

1. Stop the containers

```bash
cd ../docker
docker compose down -v --remove-orphans
```
