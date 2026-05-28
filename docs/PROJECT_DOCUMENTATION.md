# Student Performance Advisor — Project Documentation

## Project Summary

Student Performance Advisor is a rule-based expert system designed to assess student academic risk and provide personalized recommendations. It combines a Python expert system backend with a modern React frontend, enabling both API-driven analysis and interactive UI usage.

## System Architecture

The project is structured into the following major layers:

1. **Frontend** (`frontend/`)
   - React application built with Vite
   - Uses `axios` to call the Flask backend
   - Provides input forms, result cards, and sample profile loading

2. **Backend API** (`api/`)
   - Flask application exposing endpoints for health, sample profiles, and analysis
   - Loads the knowledge base once on startup for fast inference

3. **Inference Engine** (`inference_engine/`)
   - Implements a forward-chaining rule engine
   - Uses working memory, rule evaluation, conflict resolution, and certainty factors

4. **Knowledge Base** (`knowledge_base/`)
   - Encapsulates expert rules for attendance, academics, behavior, and intervention
   - Rules add conclusions to working memory as they fire

5. **Input Handling** (`input_handler/`)
   - Defines `StudentProfile` model
   - Validates all input fields with hard errors and warnings

6. **Output Handling** (`output_handler/`)
   - `RecommendationProcessor` formats results and identifies risk factors, strengths, and risk score
   - `ReportGenerator` creates both console and UI-friendly reports

7. **Tests** (`tests/`)
   - `tests/test_scenarios.py` includes 10 sample student scenarios, validation checks, and result summaries

## Data Flow

1. User submits student profile data through the frontend or API client.
2. Backend receives JSON payload at `/api/analyze`.
3. Data is converted into a `StudentProfile`, validated, and converted to a dictionary.
4. Inference engine loads the facts into working memory.
5. Rules are evaluated and fired using conflict resolution.
6. The engine returns raw conclusions and reasoning trace.
7. Recommendations and reports are processed and returned by the API.

## Expert System Details

### Inference Engine

- Uses **forward chaining** to infer conclusions from student facts.
- Keeps track of fired rules to avoid duplicate firing.
- Uses a maximum iteration guard to prevent infinite loops.
- Resolves conflicts by rule priority and certainty factor.

### Rule Base

The knowledge base contains the following rule categories:

- Attendance rules
- Academic performance rules
- Behavioral risk rules
- Composite/conflict rules
- Recommendation rules

Rules are built with:
- `name`
- `conditions`
- `actions`
- `cf` (certainty factor)
- `priority`
- `description`

### Certainty Factor Logic

The engine supports certainty factor reasoning to express confidence in each conclusion and to combine supporting evidence.

## Input Validation

`input_handler/input_validator.py` verifies:

- Required fields are present
- Scores and percentages are within 0–100
- Study hours are realistic (0–18)
- Stress level is 1–5
- Trend values are valid (`improving`, `stable`, `declining`)

Warnings are also raised for unusual but acceptable values such as zero study hours.

## API Endpoints

- `GET /api/health`
  - Returns service status and version.

- `GET /api/samples`
  - Returns 10 sample student profiles for testing and demo.

- `POST /api/analyze`
  - Accepts JSON student profile data.
  - Returns performance verdict, risk score, strengths, risk factors, recommendations, and reasoning trace.

## Running the System

### Backend

From repository root:

```bash
python api/app.py
```

Or use the helper command:

```bash
python main.py flask
```

### Frontend

From `frontend/`:

```bash
npm install
npm run dev
```

### Demo Mode

Run a terminal demo without starting the frontend:

```bash
python main.py demo
```

### Test Suite

Execute all scenario tests:

```bash
python main.py test
```

## Project Structure

- `api/`
  - `app.py` — Flask app factory and server entrypoint
  - `routes/` — API route blueprints
  - `config.py` — environment and Flask configuration

- `frontend/`
  - React UI source code, package configuration, and Vite setup

- `inference_engine/`
  - `engine.py` — inference engine, facts, rules, conflict resolver

- `knowledge_base/`
  - `rules.py` — expert rules and knowledge base builder

- `input_handler/`
  - `student_profile.py` — student profile model
  - `input_validator.py` — validator logic

- `output_handler/`
  - `recommendation.py` — recommendation formatting and risk scoring
  - `report_generator.py` — formatted text/UI data generation

- `tests/`
  - `test_scenarios.py` — sample student test scenarios and runner

- `ui/`
  - `app.py` — Streamlit interface entrypoint

## Maintenance and Improvements

### Suggested next steps

- Add automated unit tests for validator, engine, and processor modules.
- Expand frontend result visualizations and historical tracking.
- Add Docker support for backend and frontend.
- Improve rule explainability with more detailed trace metadata.

### Known gaps

- The current project depends on local environment setup for both Python and Node.
- `frontend/node_modules/` should remain local and is ignored by `.gitignore`.
- The system is advisory and should not replace official academic counseling.
