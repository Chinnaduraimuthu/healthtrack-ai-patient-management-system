# HealthTrack – AI Patient Management System

An AI-powered patient management application built using Python Flask, SQLite, and Google Gemini AI. HealthTrack allows users to manage patient records, perform CRUD operations, validate health information, and generate AI-powered educational remarks based on laboratory measurements.

## Project Overview

HealthTrack is developed as part of the Gokul Infocare AI Growth & Automation Associate – Task 2 assessment.

The application provides a user-friendly dashboard for managing patient information and generating AI-assisted health insights.

The system stores patient records persistently using SQLite and integrates Google Gemini AI to generate educational remarks based on glucose, haemoglobin, and cholesterol measurements.

**Important:** AI-generated remarks are for educational purposes only and are not medical diagnoses.

## Features

### 1. Patient Management (CRUD)

- Create new patient records.
- View all registered patients.
- View individual patient information.
- Update existing patient details.
- Delete patient records.

### 2. Patient Information

The application collects:

- Full Name
- Date of Birth
- Email Address
- Glucose
- Haemoglobin
- Cholesterol
- AI-generated Remarks

### 3. Input Validation

- Required field validation.
- Email format validation.
- Date of birth validation.
- Future date rejection.
- Numeric value validation.
- Non-negative laboratory measurement validation.

### 4. Gemini AI Integration

- Integrates Google Gemini AI through its REST API.
- Generates educational remarks based on patient laboratory measurements.
- Saves generated remarks in the SQLite database.
- Handles temporary API errors and retries selected server errors.
- Includes safeguards against presenting AI output as a medical diagnosis.

### 5. Dashboard UI

- Clean and responsive dashboard.
- Sage & Emerald colour theme.
- Light and Dark mode.
- Patient card layout.
- Patient search functionality.
- Health measurement summaries.
- AI-generated remarks display.

## Technology Stack

| Technology       | Purpose                         |
| ---------------- | ------------------------------- |
| Python           | Backend programming             |
| Flask            | Web framework and REST API      |
| SQLite           | Persistent database             |
| HTML5            | Frontend structure              |
| CSS3             | Styling and responsive design   |
| JavaScript       | Frontend interactions           |
| Google Gemini AI | AI-generated health remarks     |
| Requests         | External API integration        |
| python-dotenv    | Environment variable management |

## Project Structure

```text
healthtrack-ai-patient-management-system/
│
├── app.py
├── database.py
├── import_data.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
└── instance/
    └── healthtrack.db
```

The SQLite database is created locally when the application initializes. The database file is excluded from GitHub.

## Installation and Setup

### Prerequisites

- Python 3.10 or later
- Git
- Google Gemini API key
- VS Code or another code editor

### Step 1: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate into the project directory:

```bash
cd healthtrack-ai-patient-management-system
```

### Step 2: Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure environment variables

Create a `.env` file in the project root directory.

Add the following configuration:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_MODEL=gemini-3.5-flash-lite
```

Replace `YOUR_GEMINI_API_KEY` with your actual Gemini API key.

**Security:** Never upload your actual `.env` file or API key to GitHub.

### Step 5: Initialize the database

The database is automatically initialized when the Flask application starts.

### Step 6: Import assessment records

If the database is empty, run:

```bash
python import_data.py
```

This imports the 10 assessment patient records.

Run the import script only when the database is empty.

### Step 7: Start the application

```bash
python app.py
```

Open the application in your browser:

```text
http://127.0.0.1:5000/
```

## API Endpoints

The application provides the following REST API endpoints:

| Method | Endpoint                     | Description            |
| ------ | ---------------------------- | ---------------------- |
| GET    | `/api/health`                | Check backend status   |
| GET    | `/api/patients`              | Retrieve all patients  |
| POST   | `/api/patients`              | Create a patient       |
| GET    | `/api/patients/<id>`         | Retrieve one patient   |
| PUT    | `/api/patients/<id>`         | Update patient details |
| DELETE | `/api/patients/<id>`         | Delete a patient       |
| POST   | `/api/patients/<id>/analyze` | Generate AI remarks    |

## AI Integration Workflow

1. The user selects a patient from the dashboard.
2. The frontend sends an analysis request to the Flask backend.
3. Flask retrieves the patient's laboratory measurements from SQLite.
4. The backend sends the measurements to Google Gemini AI.
5. Gemini generates educational health remarks.
6. Flask saves the generated remarks in SQLite.
7. The frontend displays the generated remarks.

## Data Storage

HealthTrack uses SQLite for persistent storage.

Patient information and AI-generated remarks are stored in the local database.

The database is initialized automatically by the application.

## Testing

The application was tested for:

- Patient creation.
- Patient record retrieval.
- Patient information updates.
- Patient deletion.
- Invalid email validation.
- Invalid and future date validation.
- Numeric measurement validation.
- Gemini AI integration.
- AI remarks persistence.
- Light and Dark mode.
- Database persistence after restarting the application.

## Medical Disclaimer

AI-generated information is intended for educational purposes only and is not a medical diagnosis.

Laboratory measurements cannot be interpreted accurately without their measurement units, laboratory reference ranges, medical history, symptoms, and professional clinical evaluation.

Users should consult qualified healthcare professionals for medical advice and interpretation of laboratory results.

## Future Improvements

- User authentication and role-based access.
- Patient report generation and PDF export.
- Improved health data visualization.
- Additional AI-assisted health information.
- Cloud database integration.
- Application deployment.

## Author

**Chinnadurai P**

Computer Science and Engineering Graduate

- LinkedIn: [https://www.linkedin.com/in/chinnadurai-p-muthu](https://www.linkedin.com/in/chinnadurai-p-muthu)
- Portfolio: [https://chinnadurai-portfolio.vercel.app/](https://chinnadurai-portfolio.vercel.app/)

---

**HealthTrack – Making Patient Information Management Smarter with AI.**
