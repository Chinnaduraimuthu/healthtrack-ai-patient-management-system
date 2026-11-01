
import os
import re
import math
import time
import logging

from datetime import datetime, date

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from database import (
    init_db,
    get_all_patients,
    get_patient,
    create_patient,
    update_patient,
    delete_patient,
    update_patient_remarks
)


# ==========================================
# APPLICATION CONFIGURATION
# ==========================================

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY",
    "development-only-change-before-deployment"
)

logging.basicConfig(level=logging.INFO)


# ==========================================
# PATIENT VALIDATION
# ==========================================

def validate_patient(data):

    errors = {}

    required_fields = [
        "full_name",
        "date_of_birth",
        "email",
        "glucose",
        "haemoglobin",
        "cholesterol"
    ]

    # Check required fields
    for field in required_fields:
        if data.get(field) is None or str(data.get(field)).strip() == "":
            errors[field] = "This field is required."

    if errors:
        return errors, None

    # Validate full name
    full_name = str(data["full_name"]).strip()

    if len(full_name) > 100:
        errors["full_name"] = "Name must be 100 characters or fewer."

    # Validate email
    email = str(data["email"]).strip()

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        errors["email"] = "Enter a valid email address."

    # Validate date of birth
    dob_value = str(data["date_of_birth"]).strip()
    parsed_dob = None

    supported_formats = (
        "%d/%m/%Y",
        "%d.%m.%Y",
        "%Y-%m-%d"
    )

    for date_format in supported_formats:
        try:
            parsed_dob = datetime.strptime(
                dob_value,
                date_format
            ).date()
            break
        except ValueError:
            continue

    if parsed_dob is None:
        errors["date_of_birth"] = (
            "Enter a valid date using DD/MM/YYYY or DD.MM.YYYY."
        )

    elif parsed_dob > date.today():
        errors["date_of_birth"] = (
            "Date of birth cannot be in the future."
        )

    # Validate blood-test values
    numeric_values = {}

    for field in ["glucose", "haemoglobin", "cholesterol"]:

        try:
            value = float(data[field])

            if not math.isfinite(value) or value < 0:
                raise ValueError

            numeric_values[field] = value

        except (ValueError, TypeError):
            errors[field] = "Enter a valid non-negative number."

    if errors:
        return errors, None

    # Clean validated data
    cleaned_data = {
        "full_name": full_name,
        "date_of_birth": parsed_dob.isoformat(),
        "email": email,
        "glucose": numeric_values["glucose"],
        "haemoglobin": numeric_values["haemoglobin"],
        "cholesterol": numeric_values["cholesterol"],
        "remarks": str(data.get("remarks", "")).strip()
    }

    return {}, cleaned_data


# ==========================================
# GEMINI AI HEALTH REMARKS
# ==========================================

def generate_health_remarks(patient):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "Gemini API key is missing. Check your .env file."
        )

    model = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.5-flash-lite"
    )

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        f"models/{model}:generateContent"
    )

    # Educational health-information prompt
    prompt = f"""
You are providing cautious, educational health information.

Review the following laboratory measurements:

Glucose: {patient['glucose']}
Haemoglobin: {patient['haemoglobin']}
Cholesterol: {patient['cholesterol']}

Important instructions:

1. Do not diagnose any disease.
2. The measurement units and laboratory reference ranges
   have not been provided.
3. Do not assume units or claim that a condition is confirmed.
4. Explain that a qualified healthcare professional should
   interpret the results using appropriate reference ranges.
5. Mention that symptoms and medical history are also relevant.
6. Provide a short response in plain English.
7. Clearly state that this information is educational
   and is not a medical diagnosis.
"""

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 180
        }
    }

    response = None

    # Retry temporary Gemini server errors
    for attempt in range(3):

        try:
            response = requests.post(
                url,
                headers={
                    "x-goog-api-key": api_key,
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=45
            )

        except requests.RequestException:
            # Let the route log and handle the connection error
            raise

        # Retry temporary server errors
        if response.status_code not in (503, 500):
            break

        if attempt < 2:

            wait_seconds = 2 ** (attempt + 1)

            app.logger.warning(
                "Gemini returned HTTP %s. Retrying in %s seconds.",
                response.status_code,
                wait_seconds
            )

            time.sleep(wait_seconds)

    # Check whether a response was received
    if response is None:
        raise RuntimeError("No response received from Gemini.")

    # Handle API errors
    if not response.ok:

        app.logger.error(
            "Gemini API returned HTTP %s: %s",
            response.status_code,
            response.text[:500]
        )

        raise RuntimeError(
            f"Gemini API error ({response.status_code}). "
            "Check your API key, model name, and API availability."
        )

    # Extract AI-generated remarks
    try:

        result = response.json()

        remarks = (
            result["candidates"][0]
            ["content"]["parts"][0]["text"]
        ).strip()

        if not remarks:
            raise ValueError("Empty AI response.")

        return remarks

    except (KeyError, IndexError, TypeError, ValueError):

        raise RuntimeError(
            "Gemini returned an unexpected or empty response."
        )


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================================
# HEALTH CHECK
# ==========================================

@app.route("/api/health", methods=["GET"])
def health_check():

    return jsonify({
        "success": True,
        "status": "ok",
        "message": "Gokul Infocare Task 2 backend is running."
    })


# ==========================================
# READ ALL PATIENTS
# ==========================================

@app.route("/api/patients", methods=["GET"])
def list_patients():

    patients = get_all_patients()

    return jsonify({
        "success": True,
        "count": len(patients),
        "patients": patients
    })


# ==========================================
# CREATE PATIENT
# ==========================================

@app.route("/api/patients", methods=["POST"])
def add_patient():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):

        return jsonify({
            "success": False,
            "message": "Send patient information as JSON."
        }), 400

    errors, cleaned_data = validate_patient(data)

    if errors:

        return jsonify({
            "success": False,
            "errors": errors
        }), 400

    patient_id = create_patient(cleaned_data)

    return jsonify({
        "success": True,
        "message": "Patient created successfully.",
        "patient_id": patient_id
    }), 201


# ==========================================
# READ ONE PATIENT
# ==========================================

@app.route("/api/patients/<int:patient_id>", methods=["GET"])
def view_patient(patient_id):

    patient = get_patient(patient_id)

    if not patient:

        return jsonify({
            "success": False,
            "message": "Patient not found."
        }), 404

    return jsonify({
        "success": True,
        "patient": patient
    })


# ==========================================
# UPDATE PATIENT
# ==========================================

@app.route("/api/patients/<int:patient_id>", methods=["PUT"])
def edit_patient(patient_id):

    if not get_patient(patient_id):

        return jsonify({
            "success": False,
            "message": "Patient not found."
        }), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):

        return jsonify({
            "success": False,
            "message": "Send patient information as JSON."
        }), 400

    errors, cleaned_data = validate_patient(data)

    if errors:

        return jsonify({
            "success": False,
            "errors": errors
        }), 400

    update_patient(patient_id, cleaned_data)

    return jsonify({
        "success": True,
        "message": "Patient updated successfully."
    })


# ==========================================
# GEMINI AI ANALYSIS
# ==========================================

@app.route(
    "/api/patients/<int:patient_id>/analyze",
    methods=["POST"]
)
def analyze_patient(patient_id):

    patient = get_patient(patient_id)

    if not patient:

        return jsonify({
            "success": False,
            "message": "Patient not found."
        }), 404

    try:

        # Generate remarks using Gemini
        remarks = generate_health_remarks(patient)

        # Save AI remarks in SQLite database
        updated = update_patient_remarks(
            patient_id,
            remarks
        )

        if not updated:

            return jsonify({
                "success": False,
                "message": "Could not save AI remarks."
            }), 500

        return jsonify({
            "success": True,
            "message": "AI remarks generated successfully.",
            "remarks": remarks
        }), 200

    except ValueError as error:

        app.logger.error("Configuration error: %s", error)

        return jsonify({
            "success": False,
            "message": str(error)
        }), 400

    except requests.RequestException as error:

        # Print the actual connection error in Flask terminal
        app.logger.exception("Gemini connection failed")

        return jsonify({
            "success": False,
            "message": "Could not connect to Gemini.",
            "error_type": type(error).__name__
        }), 502

    except RuntimeError as error:

        app.logger.exception("Gemini analysis failed")

        return jsonify({
            "success": False,
            "message": str(error)
        }), 502

    except Exception:

        app.logger.exception("Unexpected AI analysis error")

        return jsonify({
            "success": False,
            "message": "An unexpected error occurred during AI analysis."
        }), 500


# ==========================================
# DELETE PATIENT
# ==========================================

@app.route(
    "/api/patients/<int:patient_id>",
    methods=["DELETE"]
)
def remove_patient(patient_id):

    deleted = delete_patient(patient_id)

    if not deleted:

        return jsonify({
            "success": False,
            "message": "Patient not found."
        }), 404

    return jsonify({
        "success": True,
        "message": "Patient deleted successfully."
    })


# ==========================================
# INITIALIZE DATABASE
# ==========================================

init_db()


# ==========================================
# START APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
