# RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot built with FastAPI, React, Weaviate, and Google Gemini.

## Prerequisites

- [Docker](https://www.docker.com/) & Docker Compose
- [Python](https://www.python.org/) 3.10+
- [Node.js](https://nodejs.org/) 20+
- A [Google Cloud API Key](https://aistudio.google.com/app/apikey) for Gemini

## Setup Instructions

### 1. Infrastructure (Weaviate)

Start the vector database using Docker Compose:

```bash
docker-compose up -d
```

### 2. Backend (FastAPI)

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment and activate it:

```bash
# Linux/macOS
python -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Set up your environment variables. You need to set the `GOOGLE_API_KEY`:

```bash
# Linux/macOS
export GOOGLE_API_KEY="your_api_key_here"

# Windows (PowerShell)
$env:GOOGLE_API_KEY="your_api_key_here"
```

Start the backend server:

```bash
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`. You can view the docs at `http://localhost:8000/docs`.

### 3. Frontend (React + Vite)

Open a new terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:5173`.

## Usage

1.  Open the frontend application in your browser.
2.  Upload a PDF document using the upload area in the sidebar.
3.  Once uploaded, type your questions in the chat input.
4.  The chatbot will answer based on the content of the uploaded PDF and provide citations.

## Architecture

-   **Backend**: FastAPI following Domain-Driven Design (DDD) principles.
-   **Frontend**: React with TypeScript, Tailwind CSS, and Clean Architecture.
-   **Database**: Weaviate (Vector Store).
-   **AI**: Google Gemini (Embeddings & LLM).
