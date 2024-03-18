# Development Setup for fAIr Frontend

This should be followed after setting up the backend.

1. Create `.env` in /frontend
    ```bash
    cd frontend
    cp .env_sample .env
    ```
    You can leave it as it is for dev setup

2. Build & Run Frontend container

    ```bash
    docker compose build
    docker compose up
    ```

You can now access the frontend using URL `127.0.0.1:3000`.