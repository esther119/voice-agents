# Voice Agent MVP

A simple phone-based AI agent that collects patient appointment information using Retell AI.

## 🚀 Quick Start (2-Hour Setup)

### Prerequisites

- Python 3.8+
- Retell AI account
- ngrok (for local testing)

### 1. Setup Project

```bash
# Clone or create project directory
mkdir voice-agent-mvp
cd voice-agent-mvp

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp env.example .env
# Edit .env with your Retell AI API key
```

### 2. Get Retell AI API Key

1. Go to [Retell AI Dashboard](https://app.retellai.com)
2. Create account and get API key
3. Add to `.env` file:
   ```
   RETELL_API_KEY=your_actual_api_key_here
   ```

### 3. Run the App

```bash
# Start Flask app
python app.py
```

You should see:

```
🚀 Starting Voice Agent MVP...
📁 Data file: data.json
📝 Notifications file: notifications.txt
🌐 Health check: http://localhost:5000/health
👥 Patients endpoint: http://localhost:5000/patients
📋 Notifications endpoint: http://localhost:5000/notifications
```

### 4. Expose with ngrok (for testing)

```bash
# In another terminal
ngrok http 5000
```

Copy the ngrok URL (e.g., `https://abc123.ngrok.io`)

### 5. Configure Retell AI Agent

In your Retell AI dashboard:

**Agent Settings:**

- **Webhook URL:** `https://your-ngrok-url.ngrok.io/webhook`
- **Voice:** Choose professional female voice
- **Response Type:** Streaming

**Agent Prompt:**

```
You are a medical appointment scheduler. Your job is to collect patient information in a friendly, professional manner.

Collect these 4 pieces of information:
1. Patient's full name
2. Date of birth
3. Phone number
4. Reason for visit

Keep the conversation natural and empathetic. Once you have all 4 pieces of information, call the save_data function and politely end the call by saying someone will contact them shortly.
```

**Function Configuration:**

```json
{
  "name": "save_data",
  "description": "Save collected patient data when all information is gathered",
  "parameters": {
    "type": "object",
    "properties": {
      "name": {
        "type": "string",
        "description": "Patient's full name"
      },
      "date_of_birth": {
        "type": "string",
        "description": "Patient's date of birth"
      },
      "phone": {
        "type": "string",
        "description": "Patient's phone number"
      },
      "reason": {
        "type": "string",
        "description": "Reason for visit or chief complaint"
      }
    },
    "required": ["name", "date_of_birth", "phone", "reason"]
  }
}
```

## 📞 Testing the System

### Make a Test Call

1. Get your Retell AI phone number from the dashboard
2. Call the number
3. Have a conversation like this:

```
AI: "Hi! I'm here to help schedule your appointment. What's your name?"
You: "John Doe"
AI: "Thanks John! What's your date of birth?"
You: "March 15th, 1985"
AI: "What's your phone number?"
You: "555-123-4567"
AI: "What's the reason for your visit?"
You: "Chest pain"
AI: "Perfect! I have everything I need. Someone will contact you shortly."
```

### Check Results

**Console Output:** You'll see live notifications:

```
==================================================
🚨 NEW PATIENT CALL RECEIVED!
==================================================
📞 Name: John Doe
🎂 DOB: March 15th, 1985
📱 Phone: 555-123-4567
🩺 Reason: Chest pain
⏰ Time: 2:30 PM
==================================================
```

**Data Storage:** Check `data.json`:

```json
{
  "patients": [
    {
      "id": 1,
      "name": "John Doe",
      "date_of_birth": "March 15th, 1985",
      "phone": "555-123-4567",
      "reason": "Chest pain",
      "timestamp": "2024-01-15T14:30:00"
    }
  ]
}
```

**Notification Log:** Check `notifications.txt`:

```
[2024-01-15T14:30:00] NEW PATIENT CALL
Name: John Doe
DOB: March 15th, 1985
Phone: 555-123-4567
Reason: Chest pain
Timestamp: 2:30 PM
--------------------------------------------------
```

## 🛠 API Endpoints

- `GET /health` - Health check
- `GET /patients` - View all collected patient data
- `GET /notifications` - View notification log
- `POST /webhook` - Retell AI webhook (don't call directly)

## 📁 File Structure

```
voice-agent-mvp/
├── app.py              # Main Flask application
├── data.json           # Patient data storage
├── notifications.txt   # Team notification log
├── requirements.txt    # Python dependencies
├── env.example         # Environment variables template
└── README.md           # This file
```

## 🚨 Troubleshooting

### Common Issues

**1. Webhook not receiving data:**

- Check ngrok is running and URL is correct in Retell AI
- Verify Flask app is running on port 5000
- Check Retell AI webhook logs for errors

**2. Function not being called:**

- Verify function configuration in Retell AI matches exactly
- Check agent prompt includes instruction to call save_data
- Test with simple conversation flow

**3. Data not saving:**

- Check file permissions for data.json
- Verify Python has write access to directory
- Check Flask console for error messages

**4. No notifications appearing:**

- Check console output for emoji notifications
- Verify notifications.txt file is being created
- Look for error messages in Flask output

### Debug Mode

Run with extra debugging:

```bash
FLASK_DEBUG=1 python app.py
```

### Testing Without Phone

You can test the webhook directly:

```bash
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "function_call": {
      "name": "save_data",
      "arguments": {
        "name": "Test Patient",
        "date_of_birth": "1990-01-01",
        "phone": "555-0123",
        "reason": "Test call"
      }
    }
  }'
```

## 🎯 Success Criteria

- [ ] Phone number connects to AI agent
- [ ] Agent collects all 4 data points
- [ ] Data saves to JSON file
- [ ] Notifications appear in console and file
- [ ] Complete call takes under 5 minutes
- [ ] System works reliably for demo

## 🔮 Next Steps

After proving the MVP works:

1. **Add email notifications** (Resend integration)
2. **Deploy to Railway** for permanent hosting
3. **Add patient memory** for returning callers
4. **Implement address validation**
5. **Add appointment scheduling**
6. **Create web dashboard** for viewing data

## 📧 Support

If you run into issues:

1. Check the troubleshooting section
2. Verify all environment variables are set
3. Test with the curl command to isolate issues
4. Check Retell AI dashboard for webhook logs

---

**Goal:** Prove that AI can reliably collect patient data over the phone! 🎉
