# StoryGen AI - Project

This project is a full-stack AI application that generates children's stories and illustrations using Google's Agent Development Kit (ADK), Gemini, and Imagen.

## Features
- **AI Story Generation**: Uses Gemini 2.5 Flash to create structured 4-scene stories.
- **AI Image Generation**: Uses Imagen via a custom ADK agent to create illustrations for each scene.
- **WebSocket Communication**: Real-time updates as the story and images are being generated.
- A sleek, dark-themed interface for an immersive experience.

## Project Structure
- `backend/`: Python FastAPI backend.
  - `story_agent/`: ADK agent for text generation.
  - `story_image_agent/`: ADK agent for image generation.
  - `main.py`: Main orchestration logic and WebSocket server.
- `app/frontend/`: React-style vanilla JS frontend.
- `requirements.txt`: Python dependencies.
- `.env`: Environment configuration.

## Setup Instructions

### 1. Prerequisites
- Python 3.9+
- Google Cloud Project with Vertex AI (Imagen) enabled.
- Gemini API Key from [Google AI Studio](https://aistudio.google.com/).

### 2. Installation
```bash
# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Edit the `.env` file and provide your credentials:
```env
GOOGLE_API_KEY=your_gemini_api_key
GOOGLE_CLOUD_PROJECT_ID=your_gcp_project_id
GENMEDIA_BUCKET=your_gcs_bucket_name
```

### 4. Running the Project
```bash
# Start the backend
python backend/main.py
```
Then open `app/frontend/index.html` in your browser. (Note: In a production setup, you would serve this via a web server).

## Evaluation
You can run ADK evaluations using the provided JSON files in the `backend/` directory:
- `story_agent_eval.evalset.json`
- `test_config.json`

Run:
```bash
adk eval run --eval-set backend/story_agent_eval.evalset.json --config backend/test_config.json
```
