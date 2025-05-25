# app.py - Voice Agent MVP
# Handles Retell AI webhooks and patient data collection

from flask import Flask, request, jsonify
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# File paths
DATA_FILE = "data.json"
NOTIFICATIONS_FILE = "notifications.txt"


def load_data():
    """Load patient data from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"patients": []}


def save_data(data):
    """Save patient data to JSON file"""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def notify_team(patient_data):
    """Send notifications via console and file"""
    timestamp = datetime.now().strftime("%I:%M %p")

    # Console notification with emoji for visibility
    print("\n" + "=" * 50)
    print("🚨 NEW PATIENT CALL RECEIVED!")
    print("=" * 50)
    print(f"📞 Name: {patient_data.get('name', 'N/A')}")
    print(f"🎂 DOB: {patient_data.get('date_of_birth', 'N/A')}")
    print(f"📱 Phone: {patient_data.get('phone', 'N/A')}")
    print(f"🩺 Reason: {patient_data.get('reason', 'N/A')}")
    print(f"⏰ Time: {timestamp}")
    print("=" * 50)

    # File notification for persistence
    with open(NOTIFICATIONS_FILE, "a") as f:
        f.write(f"\n[{datetime.now().isoformat()}] NEW PATIENT CALL\n")
        f.write(f"Name: {patient_data.get('name', 'N/A')}\n")
        f.write(f"DOB: {patient_data.get('date_of_birth', 'N/A')}\n")
        f.write(f"Phone: {patient_data.get('phone', 'N/A')}\n")
        f.write(f"Reason: {patient_data.get('reason', 'N/A')}\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write("-" * 50 + "\n")


@app.route("/webhook", methods=["POST"])
def retell_webhook():
    """Main webhook endpoint for Retell AI"""
    try:
        # Get data from Retell
        request_data = request.get_json()
        print(f"📥 Received webhook data: {request_data}")

        # Handle different types of webhook events
        if request_data and "event" in request_data:
            event_type = request_data["event"]

            if event_type == "call_started":
                print("📞 Call started")
                return jsonify({"status": "call_started"})

            elif event_type == "call_ended":
                print("📞 Call ended")
                return jsonify({"status": "call_ended"})

        # Handle function calls (when AI collects patient data)
        if "function_call" in request_data:
            function_name = request_data["function_call"].get("name")

            if function_name == "save_data":
                patient_data = request_data["function_call"].get("arguments", {})

                # Load existing data
                data = load_data()

                # Add new patient with auto-increment ID
                patient_data["id"] = len(data["patients"]) + 1
                patient_data["timestamp"] = datetime.now().isoformat()
                data["patients"].append(patient_data)

                # Save to JSON file
                save_data(data)
                print(f"💾 Saved patient data: {patient_data}")

                # Notify team
                notify_team(patient_data)

                return jsonify(
                    {"success": True, "message": "Patient data saved successfully"}
                )

        # Default response for other webhook events
        return jsonify({"status": "received"})

    except Exception as e:
        error_msg = f"Error processing webhook: {str(e)}"
        print(f"❌ {error_msg}")
        return jsonify({"error": error_msg}), 500


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify(
        {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service": "Voice Agent MVP",
        }
    )


@app.route("/patients", methods=["GET"])
def get_patients():
    """Get all patients (for debugging)"""
    try:
        data = load_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/notifications", methods=["GET"])
def get_notifications():
    """Get notification log (for debugging)"""
    try:
        if os.path.exists(NOTIFICATIONS_FILE):
            with open(NOTIFICATIONS_FILE, "r") as f:
                return {"notifications": f.read()}
        return {"notifications": "No notifications yet"}
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("🚀 Starting Voice Agent MVP...")
    print(f"📁 Data file: {DATA_FILE}")
    print(f"📝 Notifications file: {NOTIFICATIONS_FILE}")
    print("🌐 Health check: http://localhost:5000/health")
    print("👥 Patients endpoint: http://localhost:5000/patients")
    print("📋 Notifications endpoint: http://localhost:5000/notifications")
    print("-" * 50)

    app.run(host="0.0.0.0", port=5000, debug=True)
