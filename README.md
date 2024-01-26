## Babuji

## Development

Follow the steps given below to run the babuji app locally on your system:

1. Install [`docker`](https://docs.docker.com/engine/install/) if you don't have it installed already.

2. Once installed, create a new file `.env` in the `api/` directory that should contain your OpenAI Key. You can use the following command to do this:

```bash
cd api/ && echo "OPENAI_API_KEY=sk-xxx" > .env
```

Note: Make sure top replace the dummmy OpenAI key with your original key.

3. Final step is to run the docker container. You can run the following command from the root directory:

```bash
docker-compose up --build
```

Once done, you will see the app up and running at http://localhost:3000. On app startup, you will notice that it will ingest all the data from `data.txt` so app load might be a bit slower for the first time.
