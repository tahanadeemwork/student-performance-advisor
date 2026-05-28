# Student Performance Advisor

A rule-based expert system that predicts student academic performance and generates personalized intervention recommendations.

## Overview

This project combines a Python-based forward-chaining expert system with a React frontend. It evaluates student performance using academic, attendance, behavioral, and personal factors to determine risk, identify strengths, and suggest actionable recommendations.

## Key Features

- Rule-based inference engine with certainty factors
- Structured student profile validation
- Flask API backend with analysis and sample routes
- React + Vite frontend for interactive input and results display
- Console reporting and recommendation generation
- Built-in scenario test suite with 10 sample student profiles

## Repository Layout

- `api/` — Flask backend routes and configuration
- `frontend/` — React application with UI and API service
- `inference_engine/` — Expert system engine, rules, and knowledge base
- `input_handler/` — Student profile model and validation logic
- `knowledge_base/` — Rule definitions used by the inference engine
- `output_handler/` — Recommendation and report generation
- `tests/` — Test scenarios and suite runner
- `ui/` — Streamlit interface entry point
- `docs/` — Project documentation and test-case reports

## Installation

### Backend

1. Create a Python virtual environment:

```bash
python -m venv .venv
```

2. Activate the environment:

```powershell
.venv\Scripts\Activate.ps1
```

3. Install requirements:

```bash
pip install -r requirements.txt
```

### Frontend

1. Change into the frontend folder:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

## Running the Project

### Run the Flask API

From the repository root:

```bash
python api/app.py
```

Or with the helper command:

```bash
python main.py flask
```

Then visit `http://localhost:5000/api/health`.

### Run the React Frontend

From `frontend/`:

```bash
npm run dev
```

Open the Vite URL shown in the terminal, usually `http://localhost:5173`.

### Run the Streamlit UI

From the repository root:

```bash
python main.py streamlit
```

### Run the Demo

```bash
python main.py demo
```

### Run the Test Suite

```bash
python main.py test
```

## API Endpoints

- `GET /api/health` — health check
- `GET /api/samples` — sample student profiles
- `POST /api/analyze` — analyze a student profile

## Documentation

- `docs/PROJECT_DOCUMENTATION.md` — full project documentation
- `docs/TEST_CASES.md` — test case definitions and scenario guidance

## GitHub

This repository is configured with a remote origin and can be pushed using Git.

## Notes

- Use `.vscode/` and `frontend/node_modules/` as local-only directories.
- The system is advisory only and should be used alongside academic counseling.

