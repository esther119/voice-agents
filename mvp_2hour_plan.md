# Voice Agent 2-Hour MVP Plan

**Goal:** Working phone number that collects patient data and logs notifications

## Absolute Minimum Scope

### What We're Building:

- ✅ Working phone number (Retell AI)
- ✅ Basic data collection (name, DOB, complaint)
- ✅ Simple storage (JSON file)
- ✅ Console/file notifications (no email complexity)
- ✅ One webhook endpoint

### What We're NOT Building:

- ❌ Email services (too much setup time)
- ❌ Supabase database (too much setup)
- ❌ Patient memory/recognition (later)
- ❌ Address validation (later)
- ❌ Appointment scheduling (later)
- ❌ Error handling (later)

## 2-Hour Timeline

### Hour 1: Core Setup (60 minutes)

- **0-15 min:** Retell AI account + agent configuration
- **15-30 min:** Flask app skeleton + ngrok setup
- **30-45 min:** Basic webhook receiving data from Retell
- **45-60 min:** JSON file storage for collected data

### Hour 2: Polish + Demo (60 minutes)

- **60-75 min:** Console logging + file notifications
- **75-90 min:** Test complete call flow
- **90-105 min:** Deploy to Railway (if time allows)
- **105-120 min:** Demo preparation

## Ultra-Simple Tech Stack

```
Phone → Retell AI → Flask Webhook → JSON File → Console Log
```

## Project Structure (Minimal)

```
voice-agent-mvp/
├── app.py              # Single Flask file (80 lines max)
├── data.json           # Patient data storage
├── notifications.txt   # Team notifications log
├── requirements.txt    # 3 dependencies only
├── .env                # Environment variables
└── README.md           # Quick setup instructions
```

## Flask App (Single File)

```python
# app.py - Everything in one file for speed

from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# Simple JSON file storage
DATA_FILE = 'data.json'
NOTIFICATIONS_FILE = 'notifications.txt'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"patients": []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def notify_team(patient_data):
    # Console notification
    print("\n🚨 NEW PATIENT CALL:")
    print(f"Name: {patient_data['name']}")
    print(f"DOB: {patient_data['date_of_birth']}")
    print(f"Phone: {patient_data['phone']}")
    print(f"Reason: {patient_data['reason']}")
    print(f"Time: {datetime.now().strftime('%I:%M %p')}")
    print("-" * 40)

    # File notification
    with open(NOTIFICATIONS_FILE, 'a') as f:
        f.write(f"\n[{datetime.now()}] NEW PATIENT:\n")
        f.write(f"Name: {patient_data['name']}\n")
        f.write(f"DOB: {patient_data['date_of_birth']}\n")
        f.write(f"Phone: {patient_data['phone']}\n")
        f.write(f"Reason: {patient_data['reason']}\n")
        f.write("-" * 40 + "\n")

@app.route('/webhook', methods=['POST'])
def retell_webhook():
    try:
        # Get data from Retell
        request_data = request.get_json()

        # Extract patient data from function call
        if 'function_call' in request_data:
            patient_data = request_data['function_call']['arguments']

            # Load existing data
            data = load_data()

            # Add new patient
            patient_data['id'] = len(data['patients']) + 1
            patient_data['timestamp'] = datetime.now().isoformat()
            data['patients'].append(patient_data)

            # Save to JSON
            save_data(data)

            # Notify team
            notify_team(patient_data)

            return jsonify({"success": True})

        return jsonify({"success": True})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
```

## Retell AI Agent Config (15 minutes)

### Agent Prompt:

```
You are a medical appointment scheduler. Collect:
1. Patient name
2. Date of birth
3. Phone number
4. Reason for visit

Keep it simple and friendly. When you have all 4 pieces of information,
call the save_data function and end the call politely.
```

### Single Function:

```json
{
  "name": "save_data",
  "description": "Save collected patient data",
  "parameters": {
    "name": "string",
    "date_of_birth": "string",
    "phone": "string",
    "reason": "string"
  }
}
```

## Data Storage (JSON File)

```json
{
  "patients": [
    {
      "id": 1,
      "name": "John Doe",
      "date_of_birth": "1985-03-15",
      "phone": "555-1234",
      "reason": "Chest pain",
      "timestamp": "2024-01-15T10:30:00Z"
    }
  ]
}
```

## Notification System (Console + File)

**Console Output:**

```
🚨 NEW PATIENT CALL:
Name: John Doe
DOB: 1985-03-15
Phone: 555-1234
Reason: Chest pain
Time: 10:30 AM
----------------------------------------
```

**File Log (notifications.txt):**

```
[2024-01-15 10:30:00] NEW PATIENT:
Name: John Doe
DOB: 1985-03-15
Phone: 555-1234
Reason: Chest pain
----------------------------------------
```

## Required Environment Variables

```
RETELL_API_KEY=your_retell_key
```

## Requirements.txt (Minimal)

```
Flask==2.3.3
python-dotenv==1.0.0
requests==2.31.0
```

## Testing Strategy (10 minutes)

1. **Call the number** → Should connect to Retell
2. **Give patient info** → Should trigger webhook
3. **Check console** → Should see notification printed
4. **Check data.json** → Should contain patient data
5. **Check notifications.txt** → Should have logged notification

## Demo Script (5 minutes)

**Call flow:**

```
AI: "Hi! I'm here to help schedule your appointment. What's your name?"
You: "John Doe"
AI: "Thanks John! What's your date of birth?"
You: "March 15th, 1985"
AI: "What's your phone number?"
You: "555-1234"
AI: "What's the reason for your visit?"
You: "Chest pain"
AI: "Perfect! I have everything I need. Someone will contact you shortly."
```

**Show results:**

1. **Console output** → Live notification during call
2. **Open data.json** → Patient data saved
3. **Open notifications.txt** → Team notification logged
4. **Total time:** Under 5 minutes for complete intake

## Success Criteria

- [ ] Phone number works and connects
- [ ] Can collect 4 basic data points
- [ ] Data saves to JSON file
- [ ] Notifications appear in console AND file
- [ ] Complete call takes under 5 minutes
- [ ] Zero crashes during demo

## If You Have Extra Time

**Priority order for additional features:**

1. Better error handling
2. Deploy to Railway
3. Add timestamp logging
4. Web interface to view data.json
5. Add email service (Resend recommended)

## Risk Mitigation

**If something breaks:**

- Retell issues → Use backup phone for demo
- Webhook issues → Show JSON file manually
- File issues → Show console output only
- Deploy issues → Demo locally with ngrok

## Post-Demo: Adding Email Later

**When ready to add emails (after proving core concept):**

1. Add Resend to requirements.txt
2. Add email function to notify_team()
3. Set RESEND_API_KEY environment variable
4. Takes 15 minutes to implement

**The goal is WORKING, not PERFECT.**

Focus on proving the core concept: AI can collect patient data reliably over the phone and notify the team instantly.
